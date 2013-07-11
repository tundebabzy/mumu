from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig

from quizzer.models import Question, Option, AnswerLogs
from quizzer.forms import OptionForm
from quizzer.tables import ReportTable

#TODO: Rewrite this view
class GenerateQuizView(TemplateView, FormMixin):
    __last_payment = None
    model = Question
    template_index = 0
    template_name = ['quiz_page.html', 'answer_page.html',
                                                'upgrade-package.html']
    success_url = '/quiz/explanation/'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenerateQuizView, self).dispatch(*args, **kwargs)

    def get_template_index(self):
        if self.template_index is None:
            raise ImproperlyConfigured(
                "GenerateQuizView requires a definition of template_index"
                "which should be the index of the template to be rendered"
                "from template_name list")
        return self.template_index
    
    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        return [self.template_name[self.get_template_index()]]

    def is_valid_category(self, category):
        allowed_categories = ('exam','level','paper','topic')
        return category in allowed_categories

    def subscription_paid(self):
        user = self.request.user
        if user.is_staff:
            return True
            
        last_payment = self.get_last_payment()
        if last_payment:
            return last_payment.has_not_expired()
        else:
            return False

    def get_last_payment(self):
        user = self.request.user
        if not self.__last_payment:
            try:
                self.__last_payment = user.payment_set.order_by('-time')[0]
            except:
                pass
        return self.__last_payment

    def get_allowed_category(self):
        last_payment = self.get_last_payment()
        if last_payment:
            return last_payment.get_category_paid_for()

    def can_show(self, obj, category):
        user = self.request.user
        if user.is_staff:
            return True

        last_payment = self.get_last_payment()
        if last_payment:
            if last_payment.get_category_paid_for() == 'level':
                try:
                    return obj.level == last_payment.level
                except:
                    return False
            elif last_payment.get_category_paid_for() == 'paper' and category in ['paper', 'topic']:
                try:
                    return obj.paper == last_payment.paper
                except:
                    return False
        return False

    def query_database(self, category, identifier):
        try:
            if self.model is not None:
                question = self.model._default_manager.raw("""
                SELECT *
                FROM quizzer_question
                WHERE id = get_random_id(%s, %s)
                """,[category, identifier])[0]
                self.set_session_random_question(question)
            else:
                raise ImproperlyConfigured(u"'%s' must define 'model'"
                                           % self.__class__.__name__)
        except:
            raise Http404
            # log this as critical and send email to admin here
        return question

    def get_random_question(self, **kwargs):
        """
        Returns a random Question object
        """
        user = self.request.user
        category = kwargs['category']
        identifier = kwargs['identifier']
        
        if not self.is_valid_category(category):
            # Log this incidence then....
            raise Http404
        if not self.subscription_paid():
            self.template_index = 2
        else:
            random_question = self.query_database(category, identifier)
            if not self.can_show(random_question, category):
                raise Http404
            return random_question

    def get_option_form(self, question, data={}):
        """
        Returns an OptionForm instance.
        """
        options = OptionForm(random_question=question, data=data)
        return options

    def get_selection(self, random_question, **kwargs):
        """
        """
        selection = self.request.session.get('selection')
        lazy_query = {
            'exam': 'random_question.exam.name',
            'level': 'random_question.level.name',
            'paper': 'random_question.paper.name',
            'topic': 'random_question.topic.name',
        }   # Kept as string to avoid database hits for each dict key

        if selection:
            if self.request.session.get('category') and kwargs['category'] != self.request.session.get('category'):
                selection = self.request.session['selection'] = eval(lazy_query[kwargs['category']])
                self.set_session_category(**kwargs)
            else:
                self.set_session_category(**kwargs)
        else:
            selection = self.request.session['selection'] = eval(lazy_query[kwargs['category']])
            self.set_session_category(**kwargs)
        return selection

    def get_answer_page_context(self, data, question, option_form, **kwargs):
        question = question
        option_id = data.get('options')
        answer = get_object_or_404(Option, id=option_id)
        table = ReportTable(self.request.user.answerlogs_set.all().filter(question=question))
        RequestConfig(self.request, paginate={'per_page':10}).configure(table)

        context = {
            'question': question,
            'explanation': question.optionexplanation_set.all(),
            'links': question.link_set.all(),
            'next': self.request.path,
            'selection': self.get_selection(question, **kwargs),
            'is_correct': answer.is_true,
            'report': table
        }
        self.template_index = 1
        AnswerLogs.objects.create(user=self.request.user, question=question, answer=answer)

        return context

    def request_is_reload(self):
        # We save a Question object in the session and delete it when
        # after it has been retrieved. If there is a reload of the answer
        # page, we check to see if the question object is in the session
        # or not
        if self.request.session.get('question', None):
            return False
        return True

    def no_error_in_form(self, option_form):
        return option_form.is_valid()

    def form_check_complete(self, question_obj, option_form, **kwargs):
        # remove the Question from session
        del self.request.session['question']
        return self.get_answer_page_context(self.request.POST, question_obj, option_form, **kwargs)

    def get_question_and_options(self, data, **kwargs):
        question = self.get_session_random_question()
        if question:
            options = self.get_option_form(question, data=data)
            return (question, options)
        return (None, None)

    def get_context_data(self, **kwargs):
        if self.request.method == 'POST':
            random_question, options = self.get_question_and_options(self.request.POST, **kwargs)
            if options and self.no_error_in_form(options):
                return self.form_check_complete(random_question, options, **kwargs)
            else:
                selection = self.get_selection(random_question, **kwargs)
                context = {
                    'random_question': random_question,
                    'options': options, 'selection': selection,
                    'error': 'Please select an option'
                }
                return context
                
        random_question = self.get_random_question(**kwargs)
        if not random_question:
            return {}
        else:
            options = self.get_option_form(random_question)
            selection = self.get_selection(random_question, **kwargs)
            context = {
                'random_question': random_question, 'error': '',
                'options': options, 'selection': selection,
            }
            return context 

    def set_session_random_question(self, question):
        """
        Add random Question object to the session
        """
        self.request.session['question'] = question

    def set_session_category(self, **kwargs):
        self.request.session['category'] = kwargs['category']

    def get_session_random_question(self):
        return self.request.session.get('question')

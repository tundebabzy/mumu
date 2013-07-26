from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import utils

from lib.mixins import SessionMixin, FormExtrasMixin
from utils.utils import FormError

from quizzer.models import Option, AnswerLogs
from quizzer.forms import OptionForm

class GenerateQuizView(FormView, SessionMixin, FormExtrasMixin):
    """
    This works by querying the database for a Question and presenting it along
    with an OptionForm
    """
    form_class = OptionForm
    success_url = '/quiz/explanation/'
    template_name = ['quiz_page.html', 'answer_page.html','upgrade-package.html'] 
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenerateQuizView, self).dispatch(*args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        """
        Subclass from ProcessView. Here I add a checkpoint
        """
        self.remove_session_var(['last_answer'])
        if self.subscription_is_ok(**kwargs):
            # Just in case the user uses the browser back button and session
            # vars are already set
            self.remove_session_var(['selection', 'question', 'last_answer'])
            question = self.get_random_question(**kwargs)
            form_class = self.get_form_class()
            form = self.get_form(form_class, question)
            self.set_session_var('option', form)
            return self.render_to_response(self.get_context_data(random_question=question, options=form))
        else:
            return self.need_to_pay(2)
            
    def post(self, request, *args, **kwargs):
        """
        Here I also add a checkpoint
        """
        if self.subscription_is_ok(**kwargs):
            self.__category = kwargs['category']
            self.__identifier = kwargs['identifier']
            question = self.get_session_var('question')
            form_class = self.get_form_class()
            form = self.get_form(form_class, question)
            if form.is_valid():
                self.set_session_var('option_id', request.POST.get('options'))
                return self.form_valid(form)
            else:
                return self.form_invalid(question, form)
        else:
            return self.need_to_pay()

    def form_invalid(self, question_obj, form):
        return self.render_to_response(self.get_context_data(random_question=question_obj, 
            options=form))

    def get_form(self, form_class, question_obj=None):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_form_kwargs(question_obj))

    def get_form_kwargs(self, question_obj=None):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = super(GenerateQuizView, self).get_form_kwargs()
        if question_obj:
            kwargs.update({
                'random_question':question_obj,
                'error_class': FormError
            })
        return kwargs
            
    def get_template_names(self):
        """
        Overrides the default by using self.template_list_index to return a
        template to be used. self.template_list_index contains an int which 
        signifies the index of the template name in self.template_name that
        should be returned.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name[self.template_list_index]]
            
    def get_context_data(self, **kwargs):
        selection = self.get_selection(kwargs.get('random_question'))
        kwargs.update({'selection':selection})
        return kwargs

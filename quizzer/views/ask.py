import datetime
import random

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control

from lib.mixins import SessionMixin
from lib.utils import FormError
from quizzer.models import Option, AnswerLogs, Question, Code
from quizzer.forms import OptionForm
from lib.decoder import ExamCodeDecoder


__author__ = 'tunde'


def random_id(id_list):
    if id_list:
        id_ = random.sample(id_list, 1)
        return id_[0]
    raise Http404


class FormExtrasMixin(object):
    """
    This Mixin helps to query the database and manipulate the session for `Question` objects
    """
    model = Question
    template_list_index = 0
    valid_category = ('level','paper', 'topic')

    def is_valid_category(self, category):
        return category in self.valid_category

    def set_time(self):
        return self.set_session_var('last_query_database_time', datetime.datetime.now())

    def time_has_expired(self):
        time = self.get_session_var('last_query_database_time')
        if time:
            return datetime.datetime.now() - time > datetime.timedelta(hours=3)

    def query_database(self, category, identifier, code):
        """
        Get a list of `Question` id that is compatible with the supplied code
        and category
        """
        decoder = ExamCodeDecoder()
        qs = None

        if category == 'exam':
            qs = self.model.objects.filter(code__code__startswith=code, approved=True).values_list('id', flat=True)

        elif category == 'level' or category == 'paper':
            _qs = self.model.objects.filter(code__code__contains=code, approved=True).values_list('code', flat=True)
            temp_qs = Code.objects.filter(id__in=_qs).values_list('code', flat=True)
            code_list = decoder.filter_code_list_by_sub_code(code, temp_qs, category)
            qs = self.model.objects.filter(code__code__in=code_list, approved=True).values_list('id', flat=True)

        elif category == 'topic':
            qs = self.model.objects.filter(code__code__endswith=code, approved=True).values_list('id', flat=True)

        # Set session variables with the data
        session_key = identifier+'-'+category
        self.set_session_var(session_key, qs)
        self.set_time()

    def get_question(self, **kwargs):
        """
        Determine the code of a Question to be retrieved from the
        session and then return the Question
        """
        if not self.is_valid_category(kwargs['category']):
            print 'not valid category'
            raise Http404

        session_key = kwargs['identifier']+'-'+kwargs['category']
        if not self.get_session_var(session_key) or self.time_has_expired():
            self.query_database(kwargs['category'], kwargs['identifier'], kwargs['code'])

        question_id = random_id(self.get_session_var(session_key))
        question = self.model.objects.get(id=question_id)

        # `question` is the question displayed to the user. We persist it so it can be reused on the answer page
        self.set_session_var('question', question)

        # .... `category` 1code` and `identifier` are persisted so that they can be used to build the url for the next
        # random question on the answer page
        self.set_session_var('category', kwargs['category'])
        self.set_session_var('code', kwargs['code'])
        self.set_session_var('identifier', kwargs['identifier'])

        return question

    def get_template_names(self):
        """
        Overrides the default by using self.template_list_index to return a template to be used.
        self.template_list_index contains an int which signifies the index of the template name in self.template_name
        that should be returned.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name[self.template_list_index]]


class QuestionEngine(FormView, SessionMixin, FormExtrasMixin):
    """
    This is the engine that spurts random questions to the user. OptionForm contains the answer choices for the Question
    """
    form_class = OptionForm
    template_name = 'quiz_page.html'

    @cache_control(no_cache=True, must_revalidate=True, max_age=0)
    def get(self, request, *args, **kwargs):
        session_key = kwargs['category']+'-'+kwargs['identifier']   # This is set in FlashCardEngine.query_database
        if self.get_session_var('open-ended') or not self.get_session_var('multiple-choice'):
            self.init_session_vars([session_key, 'open-ended'], 'multiple-choice')

        score, total = '?', '?'
        question = self.get_question(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class, question)

        if self.request.user.is_authenticated():
            answer_log = AnswerLogs.objects.filter(user=self.request.user.get_profile())
            score = answer_log.filter(answer__is_correct=True).count()
            total = answer_log.count()

        return self.render_to_response(self.get_context_data(question=question.question_text,
                                                             options=form, score=score, total=total,
                                                             code=kwargs.get('code'),
                                                             category=kwargs.get('category')))

    def post(self, request, *args, **kwargs):
        question = self.get_session_var('question')
        form_class = self.get_form_class()
        form = self.get_form(form_class, question)
        if form.is_valid():
            option_id = request.POST.get('options')
            self.success_url = reverse('explanation', kwargs={'option_id': option_id})
            option = get_object_or_404(Option, id=option_id)
            if request.user.is_authenticated():
                AnswerLogs.objects.create(user=request.user.get_profile(),
                                          answer=option
                )
            return self.form_valid(form)
        else:
            return self.form_invalid(question, form, kwargs['code'],
                                     kwargs['category'])

    def form_invalid(self, question_obj, form, code, category):
        return self.render_to_response(self.get_context_data(question=question_obj.question_text,
                                                             options=form, code=code, category=category))

    def get_form(self, form_class, question_obj=None):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_form_kwargs(question_obj))

    def get_form_kwargs(self, question_obj=None):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(QuestionEngine, self).get_form_kwargs()
        if question_obj:
            kwargs.update({
                'question': question_obj,
                'error_class': FormError,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        decoder = ExamCodeDecoder()
        selection = decoder.sub_code_to_text(kwargs['code'], kwargs['category'])
        kwargs.update({'selection': selection})
        return kwargs


class QuestionView(QuestionEngine):
    def get(self, request, *args, **kwargs):
        question = self.get_question(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class, question)
        return self.render_to_response(self.get_context_data(question=question.question_text, options=form))

    def get_context_data(self, **kwargs):
        kwargs.update({'is_from_database_page': True})
        return kwargs

    def get_question(self, **kwargs):
        question = get_object_or_404(Question, id=kwargs.get('id'))
        self.set_session_var('question', question)
        return question

import random
import datetime

from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_control
from django.http import Http404

from quizzer.models import FlashCard, Code
from utils.decoder import ExamCodeDecoder
from lib.mixins import SessionMixin

__author__ = 'tunde'


class FlashCardEngineAnswer(TemplateView, SessionMixin):
    template_name = 'flashcard_flipped.html'
    model = FlashCard

    def get_context_data(self, **kwargs):
        flashcard = self.model.objects.filter(id=kwargs['id']).values('question_text', 'explanation')[0]
        if not flashcard:
            raise Http404
        kwargs.update({
            'question': flashcard['question_text'],
            'explanation': flashcard['explanation']
        })
        return kwargs


class FlashCardEngineQuestion(TemplateView, SessionMixin):
    model = FlashCard
    template_name = 'flashcard.html'

    @cache_control(no_cache=True, must_revalidate=True, max_age=0)
    def get(self, request, *args, **kwargs):
        session_key = kwargs['identifier']+'-'+kwargs['category']   # This is set in QuestionEngine.query_database
        if self.get_session_var('multiple-choice') or not self.get_session_var('open-ended'):
            self.init_session_vars([session_key, 'multiple-choice'], 'open-ended')
        return super(FlashCardEngineQuestion, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        flashcard = self.get_question(**kwargs)
        kwargs.update(
            {'flashcard_question': flashcard['question_text'],
             'id': flashcard['id']
            }
        )
        return kwargs

    def is_valid_category(self, category):
        allowed_categories = ('exam', 'level', 'paper', 'topic')
        return category in allowed_categories

    def set_time(self):
        return self.set_session_var('flashcard_query_time', datetime.datetime.now())

    def time_has_expired(self):
        time = self.get_session_var('flashcard_query_time')
        if time:
            return datetime.datetime.now() - time > datetime.timedelta(hours=3)

    def query_database(self, category, identifier, code):
        """
        Get a list of `FlashCard` ids that are compatible with the
        supplied code and category
        """
        decoder = ExamCodeDecoder()
        qs = None

        if category == 'exam':
            qs = self.model.objects.filter(code__code__startswith=code, approved=True).values_list('id', flat=True)

        elif category == 'level' or category == 'paper':
            _qs = self.model.objects.filter(code__code__contains=code).values_list('code', flat=True)
            temp_qs = Code.objects.filter(id__in=_qs).values_list('code', flat=True)
            code_list = decoder.get_code_list(code, temp_qs, category)
            qs = self.model.objects.filter(code__code__in=code_list).values_list('id', flat=True)

        elif category == 'topic':
            qs = self.model.objects.filter(code__code__endswith=code).values_list('id', flat=True)

        # Set session variables with the data
        session_key = category+'-'+identifier
        self.set_session_var(session_key, qs)
        self.set_time()

    def random_id(self, id_list):

        if id_list:
            id_ = random.sample(id_list, 1)
            return id_[0]
        raise Http404

    def get_question(self, **kwargs):
        """
        Returns a dictionary from ValuesQuerySet
        """
        if not self.is_valid_category(kwargs['category']):
            raise Http404

        session_key = kwargs['category']+'-'+kwargs['identifier']
        if not self.get_session_var(session_key) or self.time_has_expired():
            self.query_database(kwargs['category'], kwargs['identifier'], kwargs['code'])

        flashcard_id = self.random_id(self.get_session_var(session_key))
        flashcard = self.model.objects.filter(id=flashcard_id).values('id', 'question_text')[0]

        return flashcard


class FlashCardView(FlashCardEngineQuestion):
    def get(self, request, *args, **kwargs):
        return super(FlashCardEngineQuestion, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        flashcard = self.get_question(**kwargs)
        kwargs.update({'is_from_database_page': True, 'flashcard_question': flashcard['question_text']})
        return kwargs

    def get_question(self, **kwargs):
        flashcard = self.model.objects.filter(id=kwargs.get('id')).values('question_text', 'id')[0]
        return flashcard
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_control
from django.db import models
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from quizzer.models import FlashCard, Code
from utils.decoder import ExamCodeDecoder
from lib.mixins import SessionMixin, FormExtrasMixin

from random import randint
import random
import datetime

class FlashCardEngineAnswer(TemplateView, SessionMixin):
    template_name = 'flashcard_flipped.html'
    model = FlashCard

    def get_context_data(self, **kwargs):
        try:
            flashcard = self.model.objects.filter(id=kwargs['pk']).values('question_text', 'explanation')[0]
        except ObjectDoesNotExist:
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
        print request.session.keys()
        if self.get_session_var('multiple-choice') or not self.get_session_var('open-ended'):
            self.init_session_vars([kwargs['category'], 'multiple-choice'], 'open-ended')
            print request.session.keys()
            print 'yes'
        else:
            print 'no'
        return super(FlashCardEngineQuestion, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        flashcard = self.get_question(**kwargs)
        kwargs.update(
            {'flashcard_question':flashcard['question_text'],
             'pk': flashcard['id']
             }
        )
        return kwargs

    def is_valid_category(self, category):
        allowed_categories = ('exam','level','paper','topic')
        return category in allowed_categories

    def set_time(self):
        return self.set_session_var('flashcard_query_time', datetime.datetime.now())

    def time_has_expired(self):
        time = self.get_session_var('flashcard_query_time')
        if time:
            return datetime.datetime.now() - time > datetime.timedelta(hours=3)

    def query_database(self, category, code):
        """
        Get a list of `FlashCard` ids that are compatible with the
        supplied code and category
        """
        decoder = ExamCodeDecoder()
        qs = None

        if category == 'exam':
            qs = self.model.objects.filter(code__code__startswith=code).values_list('id', flat=True)
            
        elif category == 'level' or category == 'paper':
            _qs = self.model.objects.filter(code__code__contains=code).values_list('code', flat=True)
            temp_qs = Code.objects.filter(id__in=_qs).values_list('code', flat=True)
            code_list = decoder.get_code_list(code, temp_qs, category)
            qs = self.model.objects.filter(code__code__in=code_list).values_list('id', flat=True)

        elif category == 'topic':
            qs = self.model.objects.filter(code__code__endswith=code).values_list('id', flat=True)

        # Set session variables with the data
        self.set_session_var(category, qs)
        self.set_time()

    def random_id(self, id_list):
        import itertools
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

        if not self.get_session_var(kwargs['category']) or self.time_has_expired():
            self.query_database(kwargs['category'], kwargs['code'])

        flashcard_id = self.random_id(self.get_session_var(kwargs['category']))
        f = self.model.objects.get(id=flashcard_id)
        flashcard = self.model.objects.filter(id=flashcard_id).values('id', 'question_text')[0]

        return flashcard

#class SingleFlashCardView(GenerateFlashCardView):
#    template_name = 'flashcard_nonrandom.html'
    
#    def get_object(self, queryset=None):
#        obj = DetailView.get_object(self, queryset=None)
#        return obj

#    def get_context_data(self, **kwargs):
#        return DetailView.get_context_data(self, **kwargs)


#class FlipFlashCardView(DetailView, SessionMixin):
#    model = FlashCard
#    template_name = 'flashcard_flipped.html'
        
#    def get_context_data(self, **kwargs):
#        topic_slug = self.get_session_var('topic_slug')
#        context = super(FlipFlashCardView, self).get_context_data(**kwargs)
#        if not topic_slug:
#            return context
#        context.update({'topic_slug': topic_slug})
#        return context

class FlashCardListView(ListView, FormExtrasMixin):
    template_name = 'topic_list.html'

    def get_queryset(self):
        qs = FlashCard.objects.all()
        qs = qs.order_by('topic').distinct('topic')
        qs = qs.values_list('topic_id', flat=True)
        queryset = Topic.objects.filter(id__in=qs)
        return queryset

class FlashCardView(ListView):
    template_name = 'flashcard_list.html'
    paginate_by = 50

    def get_queryset(self):
        topic_slug = self.kwargs.get('topic_slug')
        qs = FlashCard.objects.filter(topic__slug=topic_slug)
        return qs

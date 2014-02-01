from django.views.generic import DetailView, ListView
from django.views.decorators.cache import cache_control
from django.db import models

from quizzer.models import FlashCard, Topic
from lib.mixins import SessionMixin, FormExtrasMixin

from random import randint
import datetime

class GenerateFlashCardView(DetailView, SessionMixin):
    model = FlashCard
    template_name = 'flashcard.html'

    @cache_control(no_cache=True, must_revalidate=True, max_age=0)
    def get(self, request, *args, **kwargs):
        return super(GenerateFlashCardView, self).get(request, *args, **kwargs)

    def set_time(self):
        return self.set_session_var('flashcard_query_time', datetime.datetime.now())

    def time_has_expired(self):
        time = self.get_session_var('flashcard_query_time')
        if time:
            return datetime.datetime.now() - time > datetime.timedelta(hours=3)

    def query_database(self):
        qs = self.model.objects.filter(topic__slug=self.__topic_slug)
        self.set_session_var('available_flashcards', qs)
        self.set_session_var('card_count', qs.count())
        self.set_session_var('topic_slug', self.__topic_slug)
        self.set_session_var('flashcard_query_time', self.set_time())

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        """
        self.__topic_slug = self.kwargs.get('topic_slug')
        
        if not self.request.session.get('available_flashcards') or self.__topic_slug != self.get_session_var('topic_slug'):
            self.query_database()
        elif self.time_has_expired():
            self.query_database()
            
        random_number = randint(1, self.request.session.get('card_count'))
        available_flashcards = self.request.session.get('available_flashcards')
        obj = available_flashcards[random_number-1]
        
        return obj
        
    def get_context_data(self, **kwargs):
        context = super(GenerateFlashCardView, self).get_context_data(**kwargs)
        context.update({'topic_slug': self.kwargs.get('topic_slug')})
        return context

class SingleFlashCardView(GenerateFlashCardView):
    template_name = 'flashcard_nonrandom.html'
    
    def get_object(self, queryset=None):
        obj = DetailView.get_object(self, queryset=None)
        return obj

    def get_context_data(self, **kwargs):
        return DetailView.get_context_data(self, **kwargs)


class FlipFlashCardView(DetailView, SessionMixin):
    model = FlashCard
    template_name = 'flashcard_flipped.html'
        
    def get_context_data(self, **kwargs):
        topic_slug = self.get_session_var('topic_slug')
        context = super(FlipFlashCardView, self).get_context_data(**kwargs)
        if not topic_slug:
            return context
        context.update({'topic_slug': topic_slug})
        return context

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

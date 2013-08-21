from django.views.generic import DetailView, ListView
from django.db import models

from quizzer.models import FlashCard, Topic
from lib.mixins import SessionMixin, FormExtrasMixin

from random import randint

class GenerateFlashCardView(DetailView, SessionMixin):
    model = FlashCard
    template_name = 'flashcard.html'
        
    def get(self, request, *args, **kwargs):
        self.remove_session_var(['topic_slug'])
        return super(GenerateFlashCardView, self).get(request, *args, **kwargs)

    def query_database(self):
        topic_slug = self.kwargs.get('topic_slug', None)
        max_ = self.model.objects.aggregate(models.Max('id'))['id__max']
        while 1:
            try:
                random_pk = randint(1, max_)
                result = self.model.objects.filter(pk__range=(random_pk,
                    random_pk + 10), topic__slug=topic_slug)[0]
                self.set_session_var('topic_slug', topic_slug)
                return result
            except IndexError:
                pass

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        """
        obj = self.query_database()
        return obj
        
    def get_context_data(self, **kwargs):
        context = super(GenerateFlashCardView, self).get_context_data(**kwargs)
        context.update({'topic_slug': self.kwargs.get('topic_slug')})
        return context

class FlipFlashCardView(DetailView, SessionMixin):
    model = FlashCard
    template_name = 'flashcard_flipped.html'
        
    def get_context_data(self, **kwargs):
        context = super(FlipFlashCardView, self).get_context_data(**kwargs)
        context.update({'topic_slug': self.get_session_var('topic_slug')})
        return context

class FlashCardListView(ListView, FormExtrasMixin):
    template_name = 'topic_list.html'

    def get_queryset(self):
        qs = FlashCard.objects.all()
        qs = qs.order_by('topic').distinct('topic')
        qs = qs.values_list('topic_id', flat=True)
        queryset = Topic.objects.filter(id__in=qs)
        return queryset

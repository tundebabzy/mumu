from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import models

from quizzer.models import FlashCard, Topic
from lib.mixins import SessionMixin

from random import randint

class GenerateFlashCardView(DetailView, SessionMixin):
    model = FlashCard
    template_name = 'flashcard.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenerateFlashCardView, self).dispatch(*args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        self.remove_session_var(['topic_slug'])
        return super(GenerateFlashCardView, self).get(request, *args, **kwargs)

    def query_database(self):
        TIMES = 1
        topic_slug = self.kwargs.get('topic_slug', None)
        max_ = self.model.objects.aggregate(models.Max('id'))['id__max']
        i = 0
        while i < TIMES:
            try:
                random_pk = randint(1, max_)
                result = self.model.objects.filter(pk__range=(random_pk,
                    random_pk + 10), topic__slug=topic_slug)[0]
                self.set_session_var('topic_slug', topic_slug)
                return result
            except self.model.DoesNotExist:
                pass

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        """
        obj = self.query_database()
        return obj

class FlipFlashCardView(DetailView, SessionMixin):
    model = FlashCard
    template_name = 'flashcard_flipped.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FlipFlashCardView, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(FlipFlashCardView, self).get_context_data(**kwargs)
        context.update({'topic_slug': self.get_session_var('topic_slug')})
        return context

class FlashCardListView(ListView):
    template_name = 'topic_list.html'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Topic.objects.all()
        elif self.request.status.has_not_expired():
            if self.request.status.get_category_paid_for() == 'paper':
                qs = FlashCard.objects.filter(paper=self.request.status.paper)
            elif self.request.status.get_category_paid_for() == 'level':
                qs = FlashCard.objects.filter(level=self.request.status.level)
            qs = qs.order_by('topic').distinct('topic')
            qs = qs.values_list('topic_id', flat=True)
            queryset = Topic.objects.filter(id__in=qs)
        return queryset

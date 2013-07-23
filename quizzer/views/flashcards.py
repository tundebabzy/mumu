from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import models

from quizzer.models import FlashCard

from random import randint

class GenerateFlashCardView(DetailView):
    model = FlashCard
    template_name = 'flashcard.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenerateFlashCardView, self).dispatch(*args, **kwargs)

    def query_database(self):
        TIMES = 1
        topic = self.kwargs.get('topic_slug', None)
        max_ = self.model.objects.aggregate(models.Max('id'))['id__max']
        i = 0
        while i < TIMES:
            try:
                random_pk = randint(1, max_)
                return self.model.objects.filter(pk__lte=random_pk, 
                        topic__slug=topic)[0]
            except self.model.DoesNotExist:
                pass

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        obj = self.query_database()
        return obj

class FlipFlashCardView(DetailView):
    model = FlashCard
    template_name = 'flashcard_flipped.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FlipFlashCardView, self).dispatch(*args, **kwargs)


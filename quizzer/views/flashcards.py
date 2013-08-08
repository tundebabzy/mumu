from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import models

from quizzer.models import FlashCard, Topic
from lib.mixins import SessionMixin, FormExtrasMixin

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
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FlipFlashCardView, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(FlipFlashCardView, self).get_context_data(**kwargs)
        context.update({'topic_slug': self.get_session_var('topic_slug')})
        return context

class FlashCardListView(ListView, FormExtrasMixin):
#    template_name = ['topic_list.html', 'upgrade-package.html']
    template_name = 'topic_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FlashCardListView, self).dispatch(*args, **kwargs)

#    def get(self, request, *args, **kwargs):
        #if self.subscription_is_ok(**kwargs):
#        return super(FlashCardListView, self).get(request, *args, **kwargs)
        #else:
        #    return self.need_to_pay(1)

    def get_queryset(self):
#        if self.request.user.is_staff:
#            qs = FlashCard.objects.all()
#        elif self.request.status.has_not_expired():
#            if self.request.status.get_category_paid_for() == 'paper':
#                qs = FlashCard.objects.filter(paper=self.request.status.paper)
#            elif self.request.status.get_category_paid_for() == 'level':
#                qs = FlashCard.objects.filter(level=self.request.status.level)
#        else:
#            return None
        qs = FlashCard.objects.all()
        qs = qs.order_by('topic').distinct('topic')
        qs = qs.values_list('topic_id', flat=True)
        queryset = Topic.objects.filter(id__in=qs)
        return queryset

#    def get_template_names(self):
#        """
#        Overrides the default by using self.template_list_index to return a
#        template to be used. self.template_list_index contains an int which 
#        signifies the index of the template name in self.template_name that
#        should be returned.
#        """
#        if self.template_name is None:
#            raise ImproperlyConfigured(
#                "TemplateResponseMixin requires either a definition of "
#                "'template_name' or an implementation of 'get_template_names()'")
#        else:
#            return [self.template_name[self.template_list_index]]

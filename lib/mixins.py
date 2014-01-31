from quizzer.models import Question
from django.utils.timezone import make_aware, get_current_timezone
from django.db import utils, models
from django.shortcuts import Http404
import datetime
from random import randint
            
class SessionMixin(object):
    """
    This is a mixin for class based views. It provides methods to save objects
    to the session or retrieve objects from the session
    """
    def get_session_var(self, session_key):
        return self.request.session.get(session_key)
        
    def set_session_var(self, session_key, obj):
        self.request.session[session_key] = obj
        
    def remove_session_var(self, session_key):
        for key in session_key:
            if self.get_session_var(key):
                del self.request.session[key]

    def set_next_question_url_params(self, **kwargs):
        for key in kwargs:
            self.set_session_var(key, kwargs[key])
                
class FormExtrasMixin(object):
    """
    This is a mixin for class based views. It contains methods that are not
    part of the child CBV's original api.
    """
    model = Question
    template_list_index = 0
    __category = None
    __identifier = None
    
    def is_valid_category(self, category):
        allowed_categories = ('exam','level','paper','topic')
        return category in allowed_categories

    def query_database(self, category, slug):
        """
        This works with this algorithm:
        1.  Estimate a pk gap i.e an estimate of the highest possible gap 
            in the db pks.
        2.  Find the max pk value for the table.
        3.  Retrieve a queryset of objects with pk that falls in between
            a random number and the random number + gap.
        4.  If the queryset is not empty, slice the first object or else
            try again from step 3.
        """
        max_ = self.model.objects.aggregate(models.Max('id'))['id__max']
        i = 0
        qs = {}
        STARTING_NUMBER = 1
        if category == 'exam':
            qs = self.model.objects.filter(pk__range=(STARTING_NUMBER,
                max_), exam__slug=slug)
        elif category == 'level':
            qs = self.model.objects.filter(pk__range=(STARTING_NUMBER,
                max_), level__slug=slug)
        elif category == 'paper':
            qs = self.model.objects.filter(pk__range=(STARTING_NUMBER,
                max_), paper__slug=slug)
        elif category == 'topic':
            qs = self.model.objects.filter(pk__range=(STARTING_NUMBER,
                max_), topic__slug=slug)

        self.set_session_var('available_questions', qs)
        self.set_session_var('count', qs.count())
        self.set_session_var('max', max_)

    def get_question(self, **kwargs):
        self.__category = kwargs['category']
        self.__identifier = kwargs['identifier']
                                                
        if not self.is_valid_category(self.__category):
            # Log this incidence then....
            raise Http404

        # If nothing has changed in identifier
        if not self.request.session.get('available_questions') or self.__identifier != self.get_session_var('identifier'):
            self.query_database(self.__category, self.__identifier)

        self.set_next_question_url_params(category=kwargs['category'],
                identifier=kwargs['identifier'])

        random_number = randint(1, self.get_session_var('count'))
        available_question = self.get_session_var('available_questions')
        question = available_question[random_number-1]
        self.set_session_var('question', question)
        return question
        
    def get_selection(self, question):
        lazy_query = {
            'exam': 'question.exam.name',
            'level': 'question.level.name',
            'paper': 'question.paper.name',
            'topic': 'question.topic.name',
        }   # Kept as string to avoid database hits for each dict key

        selection = self.request.session.get('selection')

        if selection:
            if self.request.session.get('category') and self.__category != self.request.session.get('category'):
                self.__category = self.request.session.get('category')
                self.set_session_var('selection', eval(lazy_query[self.__category]))
            self.set_session_var('category', self.__category)
        else:
            selection = self.request.session['selection'] = eval(lazy_query[self.__category])
            self.set_session_var('category', self.__category)
        return selection

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

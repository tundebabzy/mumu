from quizzer.models import Question, Code
from django.utils.timezone import make_aware, get_current_timezone
from django.db import utils, models
from django.shortcuts import Http404
import datetime
from random import randint
from utils.decoder import ExamCodeDecoder
import random
            
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

    def init_session_vars(self, to_remove, key_to_set):
        self.remove_session_var(to_remove)
        self.set_session_var(key_to_set, True)

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
    
    def is_valid_category(self, category):
        allowed_categories = ('exam','level','paper','topic')
        return category in allowed_categories

    def set_time(self):
        return self.set_session_var('last_query_database_time', datetime.datetime.now())

    def time_has_expired(self):
        time = self.get_session_var('last_query_database_time')
        if time:
            return datetime.datetime.now() - time > datetime.timedelta(hours=3)

    def query_database(self, category, code):
        """
        Get a list of `Question` id that is compatible with the supplied code
        and category
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
        Determine the code of a Question to be retrieved from the
        session and then return the Question
        """                                                
        if not self.is_valid_category(kwargs['category']):
            raise Http404

        if not self.get_session_var(kwargs['category']) or self.time_has_expired():
            self.query_database(kwargs['category'], kwargs['code'])

        question_id = self.random_id(self.get_session_var(kwargs['category']))
        question = self.model.objects.get(id=question_id)

        # Add data to session
        # `question` is the question displayed to the user. We need to
        # persist it so it can be reused on the answer page
        self.set_session_var('question', question)

        # .... `category` 1code` and `identifier` are persisted so that 
        # they can be used to build the url for the next random question
        # on the answer page
        self.set_session_var('category', kwargs['category'])
        self.set_session_var('code', kwargs['code'])
        self.set_session_var('identifier', kwargs['identifier'])
        
        return question

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

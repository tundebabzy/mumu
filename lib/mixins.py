from quizzer.models import Question
from django.utils.timezone import make_aware, get_current_timezone
from django.db import utils
from django.shortcuts import Http404
import datetime

from utils.utils import get_last_active_payment, get_last_payment
            
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
                
class FormExtrasMixin(object):
    """
    This is a mixin for class based views. It contains methods that are not
    part of the child CBV's original api.
    """
    model = Question
    template_list_index = 0
    __last_payment =  None
    __last_active_payment = None
    __category = None
    __identifier = None
    
    def need_to_pay(self):
        self.template_list_index = 2
        return self.render_to_response({})
        
    def user_is_staff(self):
        return self.request.user.is_staff
        
    def _get_last_payment(self):
        if not self.__last_payment:
            self.__last_payment = get_last_payment(self.request)
        return self.__last_payment
        
    def _get_last_active_payment(self):
        if not self.__last_active_payment:
            self.__last_active_payment = get_last_active_payment(self.request)
        return self.__last_active_payment
        
    def subscription_is_ok(self, **kwargs):
        """
        Checks if the logged in user's payment is still active.
        """
        if self.user_is_staff():
            return True
            
        last_payment = self._get_last_active_payment()
        if last_payment:
            return last_payment.has_not_expired()
        else:
            return False

    def is_valid_category(self, category):
        allowed_categories = ('exam','level','paper','topic')
        return category in allowed_categories

    def query_database(self, category, identifier):
        try:
            if self.model is not None:
                question = self.model._default_manager.raw("""
                SELECT *
                FROM quizzer_question
                WHERE id = get_random_id(%s, %s)
                """,[category, identifier])[0]
                self.set_session_var('question', question)
            else:
                raise ImproperlyConfigured(u"'%s' must define 'model'"
                                       % self.__class__.__name__)
        except utils.DatabaseError:
            # log this as critical and send email to admin here
            raise Http404
        return question

    def can_show(self, obj, category):
        if self.user_is_staff():
            return True

        last_payment = self._get_last_active_payment()
        if last_payment:
            if last_payment.get_category_paid_for() == 'level':
                try:
                    return obj.level == last_payment.level
                except:
                    return False
            elif last_payment.get_category_paid_for() == 'paper' and category in ['paper', 'topic']:
                try:
                    return obj.paper == last_payment.paper
                except:
                    return False
        return False

    def get_random_question(self, **kwargs):
        user = self.request.user
        self.__category = kwargs['category']
        self.__identifier = kwargs['identifier']
        
        if not self.is_valid_category(self.__category):
            # Log this incidence then....
            raise Http404

        random_question = self.query_database(self.__category, self.__identifier)
        if not self.can_show(random_question, self.__category):
            raise Http404
        return random_question
        
    def get_selection(self, random_question):
        lazy_query = {
            'exam': 'random_question.exam.name',
            'level': 'random_question.level.name',
            'paper': 'random_question.paper.name',
            'topic': 'random_question.topic.name',
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

from django.views.generic import TemplateView
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from lib.mixins import SessionMixin

from quizzer.models import Login

class QuizSelectionView(TemplateView, SessionMixin):
    template_name = 'select.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuizSelectionView, self).dispatch(*args, **kwargs)
    
    def reset_quiz_session(self):
        self.remove_session_var(['selection', 'question', 'last_answer'])
            
    def get(self, request, *args, **kwargs):
        """
        There is usually a session variable called `selection` which is
        set in the `GenerateQuizView`. The session variable is deleted
        from this view.
        """
        self.reset_quiz_session()
        return super(QuizSelectionView, self).get(request, *args, **kwargs)

    # SIGNAL FIRED methods
    @receiver(user_logged_in)
    def destroy_old_session(sender, **kwargs):
        from django.contrib.sessions.models import Session

        #TODO: make this a middleware maybe?
        def get_ip_address():
            request = kwargs['request']
            ip = ''
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                parts = request.META['HTTP_X_FORWARDED_FOR'].split(',', 1)
                ip = parts[0]
            else:
                ip = request.META.get('REMOTE_ADDR', '')
            return ip
        
        user = kwargs['user']
        session_key = kwargs['request'].session.session_key
        http_user_agent = kwargs['request'].META.get('HTTP_USER_AGENT', '')
        ip_address = get_ip_address()

        # First add the present login to database
        Login.objects.create(user=user, session_key=session_key,
            http_user_agent=http_user_agent, ip_address=ip_address)

        # Get the last two latest logins
        logins = user.login_set.all().order_by('-id')[:2]
        
        l = len(logins)
        if l > 1:
            try:
                last_session_key = logins[1].session_key
                last_session = Session.objects.get(pk=last_session_key)
                last_session.delete()
            except ObjectDoesNotExist:
                # At this point, there's no previous login
                pass

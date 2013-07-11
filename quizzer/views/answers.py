from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig

from lib.mixins import SubscriptionStatusMixin, SessionMixin

from quizzer.tables import ReportTable
from quizzer.models import Option, AnswerLogs

class GradeQuestionView(TemplateView, SessionMixin, SubscriptionStatusMixin):
    """
    Processes a form which is submitted with a GET.
    """
    template_name = 'answer_page.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GradeQuestionView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        question = self.get_session_var('question')
        option_id = self.get_session_var('option_id')
        answer = get_object_or_404(Option, id=option_id)
        table = ReportTable(self.request.user.answerlogs_set.all().filter(question=question))
        RequestConfig(self.request, paginate={'per_page':10}).configure(table)
        
        kwargs.update({
        'question': question, 'is_correct': answer.is_true,
        'explanation': question.optionexplanation_set.all(),
        'links': question.link_set.all(), 'report': table,
        'selection': self.get_session_var('category'),
        'next': self.request.META.get('HTTP_REFERER', '/quiz/select/'),
        'status': self.account_status(),
        })
        if not self.get_session_var('last_answer'):
            last_answer = AnswerLogs.objects.create(user=self.request.user, question=question, answer=answer)
            self.set_session_var('last_answer', last_answer)
        return kwargs
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

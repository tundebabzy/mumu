from django.views.generic.base import TemplateView
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from lib.mixins import SessionMixin
from quizzer.models import Option, AnswerLogs


__author__ = 'tunde'


class GradeQuestionView(TemplateView, SessionMixin):
    """
    
    """
    template_name = 'answer_page.html'

    def get_context_data(self, **kwargs):
        try:
            answer = Option.objects.select_related('question').get(id=kwargs['option_id'])
        except ObjectDoesNotExist:
            raise Http404

        question = answer.question
        score = '?'
        total = '?'
        last_7 = '?'
        answer_log_7 = ''
        
        if self.request.user.is_authenticated():
            answer_log = AnswerLogs.objects.select_related().filter(user=self.request.user.get_profile())
            score = answer_log.filter(answer__is_correct=True).count()
            total = answer_log.count()
            answer_log_7 = answer_log.select_related('answer').filter(
                    answer__question=question).order_by('-time')[:7]

        
        kwargs.update({
            'question': question.question_text, 'is_correct': answer.is_correct,
            'explanation': question.explanation,
            'links': list(question.link_set.all()),
            'code': self.get_session_var('code'),
            'category': self.get_session_var('category'),
            'identifier': self.get_session_var('identifier'),
            'score': score,
            'total': total,
            'last_7': list(answer_log_7) or ''
        })

        return kwargs
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from lib.mixins import SessionMixin

from quizzer.models import Option, AnswerLogs

class GradeQuestionView(TemplateView, SessionMixin):
    """
    Processes a form which is submitted with a GET.
    """
    template_name = 'answer_page.html'

    def get_context_data(self, **kwargs):
        question = self.get_session_var('question')
        option_id = self.get_session_var('option_id')

        # If for some reason, like the user navigates away from the
        # answer page and the session variables are no longer available...
        if not question or not option_id:
            kwargs.update({
                'message': 'Something went wrong that can"t be fixed. Apologies'
            })
            self.template_name = 'answer_page_error.html'
            return kwargs
        
        answer = get_object_or_404(Option, id=option_id)

        if not self.get_session_var('last_answer') and self.request.user.is_authenticated():
            last_answer = AnswerLogs.objects.create(user=self.request.user, question=question, answer=answer)
            self.set_session_var('last_answer', last_answer)
            
        score = '?'
        
        if self.request.user.is_authenticated():
            all_answers = AnswerLogs.objects.filter(user=self.request.user)
            score = '%s/%s' %(all_answers.filter(answer__is_true=True).count(), all_answers.count())
        #last_answers = []
        
        #if self.request.user.is_authenticated():
        #    last_answers = AnswerLogs.objects.filter(user=self.request.user,
        #        question=question).order_by('time')[:4]
        
        kwargs.update({
        'question': question, 'is_correct': answer.is_true,
        'explanation': question.optionexplanation_set.all(),
        'links': question.link_set.all(),
        'selection': self.get_session_var('category'),
        #'last_answers': last_answers,
        'category': self.get_session_var('category'),
        'identifier': self.get_session_var('identifier'),
        'score': score,
        })

        
        return kwargs
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

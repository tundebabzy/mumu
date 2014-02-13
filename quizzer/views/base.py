from django.views.generic import TemplateView
from django.contrib.sites.models import get_current_site

from lib.mixins import SessionMixin

from quizzer.models import Question


class QuizSelectionView(TemplateView, SessionMixin):
    template_name = 'select.html'

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

    def get_context_data(self, **kwargs):
        questions = Question.objects.order_by('code').distinct('code')
        kwargs.update(
            {
                'distinct': questions,
                'domain': get_current_site(self.request).domain
            }
        )
        return kwargs


class FlashCardSelectionView(QuizSelectionView):
    template_name = 'topic_list.html'

from django.views.generic import TemplateView

from lib.mixins import SessionMixin

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

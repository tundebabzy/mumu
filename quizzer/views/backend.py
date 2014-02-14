from registration.backends.default.views import RegistrationView
from quizzer.forms import QuizzerForm


class QuizzerRegistrationView(RegistrationView):
    form_class = QuizzerForm

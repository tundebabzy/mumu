from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control

from lib.mixins import SessionMixin, FormExtrasMixin
from utils.utils import FormError

from quizzer.models import Option, AnswerLogs, Question
from quizzer.forms import OptionForm        

class GenerateQuizView(FormView, SessionMixin, FormExtrasMixin):
    """
    This works by querying the database for a Question and presenting it along
    with an OptionForm. OptionForm contains the answer choices for the Question
    """
    form_class = OptionForm
    success_url = '/practise/multiple-choice/answer/'  # This should not be hard-coded
    template_name = 'quiz_page.html'

    @cache_control(no_cache=True, must_revalidate=True, max_age=0)
    def get(self, request, *args, **kwargs):
        # Clean up the various session variables that might be hanging
        # around.
        self.remove_session_var(['selection', 'question', 'last_answer',
                                    'category', 'identifier'])
        question = self.get_question(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class, question)
        self.set_session_var('option', form)
        return self.render_to_response(self.get_context_data(question=question, options=form))
            
    def post(self, request, *args, **kwargs):
        question = self.get_session_var('question')
        form_class = self.get_form_class()
        form = self.get_form(form_class, question)
        if form.is_valid():
            self.set_session_var('option_id', request.POST.get('options'))
            return self.form_valid(form)
        else:
            return self.form_invalid(question, form)

    def form_invalid(self, question_obj, form):
        return self.render_to_response(self.get_context_data(question=question_obj, 
            options=form))

    def get_form(self, form_class, question_obj=None):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_form_kwargs(question_obj))

    def get_form_kwargs(self, question_obj=None):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(GenerateQuizView, self).get_form_kwargs()
        if question_obj:
            kwargs.update({
                'question':question_obj,
                'error_class': FormError
            })
        return kwargs
            
    def get_context_data(self, **kwargs):
        selection = self.get_selection(kwargs.get('question'))
        kwargs.update({'selection':selection})
        return kwargs

class QuestionView(GenerateQuizView):
    def get_context_data(self, **kwargs):
        return kwargs

    def get_question(self, **kwargs):
        question = get_object_or_404(Question, id=kwargs.get('id'))
        self.set_session_var('question', question)
        return question


class BaseMultipleChoiceQuestionList(ListView):
    model = Question
    paginate_by = 50
    template_name = 'question_list.html'
    
class LevelMultipleChoiceList(BaseMultipleChoiceQuestionList, SessionMixin):
    def get_queryset(self):
        category = self.kwargs.get('category').lower()
        identifier = self.kwargs.get('identifier').lower()
        if category == 'level':
            queryset = Question.objects.filter(level__slug__iexact=identifier)
        elif category == 'paper':
            queryset = Question.objects.filter(paper__slug__iexact=identifier)
        elif category == 'topic':
            queryset = Question.objects.filter(topic__slug__iexact=identifier)
        return queryset

    def get_context_data(self, **kwargs):
        def de_slugify(value):
            return unicode(value).strip().replace("-", " ")
            
        kwargs = super(LevelMultipleChoiceList, self).get_context_data(**kwargs)
        kwargs.update({
                'title': de_slugify(self.kwargs.get('identifier')),
                'category': self.kwargs.get('category'),
                'identifier': self.kwargs.get('identifier'),
            })
        return kwargs

from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control

from lib.mixins import SessionMixin, FormExtrasMixin
from utils.utils import FormError

from quizzer.models import Option, AnswerLogs, Question
from quizzer.forms import OptionForm
from utils.decoder import ExamCodeDecoder

class GenerateQuizView(FormView, SessionMixin, FormExtrasMixin):
    """
    This is the engine that spurts random questions to the user.
    OptionForm contains the answer choices for the Question
    """
    form_class = OptionForm
    template_name = 'quiz_page.html'

    @cache_control(no_cache=True, must_revalidate=True, max_age=0)
    def get(self, request, *args, **kwargs):
        if self.get_session_var('open-ended') or not self.get_session_var('multiple-choice'):
            print 'yes'
            self.init_session_vars([kwargs['category'], 'open-ended'], 'multiple-choice')
        else:
            print 'no'
        score = '?'
        total = '?'
        question = self.get_question(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class, question)

        if self.request.user.is_authenticated():
            answer_log = AnswerLogs.objects.filter(user=self.request.user.get_profile())
            score = answer_log.filter(answer__is_correct=True).count()
            total = answer_log.count()
        return self.render_to_response(self.get_context_data(question=question,
            options=form, score=score, total=total, code=kwargs.get('code'),
            category=kwargs.get('category')))
            
    def post(self, request, *args, **kwargs):
        """
        """
        question = self.get_session_var('question')
        form_class = self.get_form_class()
        form = self.get_form(form_class, question)
        if form.is_valid():
            option_id = request.POST.get('options')
            self.success_url = '/practise/multiple-choice/answer/%s/' % option_id
            option = get_object_or_404(Option, id=option_id)
            if request.user.is_authenticated():
                AnswerLogs.objects.create(user=request.user.get_profile(),
                    answer=option
                )
            return self.form_valid(form)
        else:
            return self.form_invalid(question, form, kwargs['code'],
                        kwargs['category'])

    def form_invalid(self, question_obj, form, code, category):
        return self.render_to_response(self.get_context_data(question=question_obj, 
            options=form, code=code, category=category))

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
        decoder = ExamCodeDecoder()
        selection = decoder.translate_sub_code(kwargs['code'], kwargs['category'])
        kwargs.update({'selection':selection})
        return kwargs

class QuestionView(GenerateQuizView):
    def get_context_data(self, **kwargs):
        kwargs.update({'is_from_database_page': True})
        return kwargs

    def get_question(self, **kwargs):
        question = get_object_or_404(Question, id=kwargs.get('id'))
        self.set_session_var('question', question)
        return question


class AllQuestionsView(ListView):
    model = Question
    paginate_by = 50
    template_name = 'question_list.html'

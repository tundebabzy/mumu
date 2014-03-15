from django.conf.urls import patterns, url
from django.views.generic import TemplateView, ListView
from quizzer.models import FlashCard, Question

from quizzer.views import (QuizSelectionView, QuestionEngine, GradeQuestionView, QuestionView,
                           FlashCardSelectionView, FlashCardEngineQuestion, FlashCardView, FlashCardEngineAnswer)

__author__ = 'tunde'

urlpatterns = patterns('',
                       url('^grade/$', GradeQuestionView.as_view(), name='grader'
                       ),

                       url('^quiz/$', TemplateView.as_view(template_name='select.html'), name='quiz_loader'

                       ),

                       #url('^how/$', TemplateView.as_view(template_name='how_it_works.html'),
                       #    name='how_it_works'
                       #),

                       url('^open-ended/$', FlashCardSelectionView.as_view(),
                           name='fcard_selection'
                       ),

                       #url('^open-ended/all/$',
                       #    ListView.as_view(model=FlashCard, template_name='flashcard_list.html', paginate_by=50),
                       #    name='all_flashcards'
                       #),

                       #url('^open-ended/all/page/(?P<page>[0-9]+)/$',
                       #    ListView.as_view(model=FlashCard, template_name='flashcard_list.html', paginate_by=50),
                       #    name='all_flashcards_paged'
                       #),

                       #url('^open-ended/(?P<id>[0-9]+)/$', FlashCardView.as_view(),
                       #    name='flashcard'),

                       #url('^open-ended/answer/(?P<id>[0-9]+)/$', FlashCardEngineAnswer.as_view(),
                       #    name='flashcard_answer_2'),

                       url('^open-ended/(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/random/(?P<code>[0-9]+)/$',
                           FlashCardEngineQuestion.as_view(), name='next_flashcard'
                       ),

                       url(
                           '^open-ended/(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/(?P<code>[0-9]+)/(?P<id>[0-9]+)/$',
                           FlashCardEngineAnswer.as_view(), name='flashcard_answer'
                       ),

                       url('^multiple-choice/$', QuizSelectionView.as_view(),
                           name='quiz_selection'
                       ),

                       #url('^multiple-choice/all/$',
                       #    ListView.as_view(model=Question, template_name='question_list.html', paginate_by=50),
                       #    name='all_questions'
                       #),

                       #url('^multiple-choice/all/page/(?P<page>[0-9]+)/$',
                       #    ListView.as_view(model=Question, template_name='question_list.html', paginate_by=50),
                       #    name='all_questions_paged'
                       #),

                       url('^multiple-choice/answer/(?P<option_id>[0-9]+)/$',
                           GradeQuestionView.as_view(), name='explanation'
                       ),

                       url('^multiple-choice/(?P<id>[0-9]+)/$', QuestionView.as_view(), name='question'),

                       url(
                           '^multiple-choice/(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/random/(?P<code>[0-9]+)/$',
                           QuestionEngine.as_view(), name='next_question'
                       ),
)
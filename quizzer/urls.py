from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from quizzer.views import (QuizSelectionView, GenerateQuizView, GradeQuestionView, AllQuestionsView, QuestionView,
                           FlashCardSelectionView, FlashCardEngineQuestion,
                           FlashCardEngineAnswer)

urlpatterns = patterns('',
                       url('^grade/$', GradeQuestionView.as_view(), name='grader'
                       ),

                       url('^how/$', TemplateView.as_view(template_name='how_it_works.html'),
                           name='how_it_works'
                       ),

                       url('^multiple-choice/$', QuizSelectionView.as_view(),
                           name='quiz_selection'
                       ),
                       url('^open-ended/$', FlashCardSelectionView.as_view(),
                           name='fcard_selection'
                       ),
                       url(
                           '^multiple-choice/(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/random/(?P<code>[0-9]+)/$',
                           GenerateQuizView.as_view(), name='next_question'
                       ),
                       url(
                           '^open-ended/(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/(?P<code>[0-9]+)/(?P<pk>[0-9]+)/$',
                           FlashCardEngineAnswer.as_view(), name='flashcard_answer'
                       ),
                       url('^open-ended/(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/random/(?P<code>[0-9]+)/$',
                           FlashCardEngineQuestion.as_view(), name='next_flashcard'
                       ),

                       url('^multiple-choice/all/page/(?P<page>[0-9]+)/$',
                           AllQuestionsView.as_view(), name='all_questions_paged'
                       ),
                       url('^multiple-choice/all/$',
                           AllQuestionsView.as_view(), name='all_questions'
                       ),
                       url('^multiple-choice/answer/(?P<option_id>[0-9]+)/$',
                           GradeQuestionView.as_view(), name='explanation'
                       ),
                       url('^multiple-choice/(?P<id>[0-9]+)/$', QuestionView.as_view(),
                           name='question'),

                       #    url('^open-ended/question/(?P<topic_slug>[-a-zA-Z]+)/$',
                       #        GenerateFlashCardView.as_view(), name='next_flashcard'
                       #    ),
                       #    url('^open-ended/answer/(?P<slug>[-a-zA-Z]+)/$',
                       #        FlipFlashCardView.as_view(), name='flashcard_flip'
                       #    ),
                       #    url('^open-ended/(?P<topic_slug>[-a-zA-Z]+)/$',
                       #        FlashCardView.as_view()
                       #    ),
                       #    url('^open-ended/(?P<pk>[0-9]+)/$',
                       #    SingleFlashCardView.as_view(), name='flashcard'
                       #    ),
                       #    url('^open-ended/$', FlashCardListView.as_view(), name='flashcard_list'
                       #    )
)

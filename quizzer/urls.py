from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
#from django.views.decorators.cache import cache_page

from quizzer.views import (QuizSelectionView, GenerateQuizView, 
    GradeQuestionView, GenerateFlashCardView, FlipFlashCardView,
    FlashCardListView, LevelMultipleChoiceList, QuestionView,
    FlashCardView, SingleFlashCardView)

urlpatterns = patterns('',
    url('^grade/$', GradeQuestionView.as_view(), name='grader'
    ),

    url('^how/$', TemplateView.as_view(template_name='how_it_works.html'),
        name='how_it_works'
    ),

    url('^multiple-choice/$', QuizSelectionView.as_view(),
        name='quiz_selection'
    ),
    url('^multiple-choice/answer/$', GradeQuestionView.as_view(), name='explanation'
    ),
    url('^multiple-choice/(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/random/$',
        GenerateQuizView.as_view(), name='next_question'
    ),
    url('^multiple-choice/(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/page/(?P<page>[0-9]+)/$',
        LevelMultipleChoiceList.as_view()
    ),
    url('^multiple-choice/(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/$',
        LevelMultipleChoiceList.as_view()
    ),
    url('^multiple-choice/(?P<id>[0-9]+)/$', QuestionView.as_view(),
        name='question'),

    url('^open-ended/question/(?P<topic_slug>[-a-zA-Z]+)/$',
        GenerateFlashCardView.as_view(), name='next_flashcard'
    ),
    url('^open-ended/answer/(?P<slug>[-a-zA-Z]+)/$',
        FlipFlashCardView.as_view(), name='flashcard_flip'
    ),
    url('^open-ended/(?P<topic_slug>[-a-zA-Z]+)/$',
        FlashCardView.as_view()
    ),
        url('^open-ended/(?P<pk>[0-9]+)/$',
        SingleFlashCardView.as_view(), name='flashcard'
    ),
    url('^open-ended/$', FlashCardListView.as_view(), name='flashcard_list'
    )
)

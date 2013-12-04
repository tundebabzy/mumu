from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
#from django.views.decorators.cache import cache_page

from quizzer.views import (QuizSelectionView, GenerateQuizView, 
    GradeQuestionView, GenerateFlashCardView, FlipFlashCardView,
    FlashCardListView, LevelMultipleChoiceList)

urlpatterns = patterns('',
    url('^multiple-choice/$', QuizSelectionView.as_view(),
        name='quiz_selection'
    ),
    url('^grade/$', GradeQuestionView.as_view(), name='grader'
    ),
    url('^multiple-choice/answer/$', GradeQuestionView.as_view(), name='explanation'
    ),
    url('^how/$', TemplateView.as_view(template_name='how_it_works.html'),
        name='how_it_works'
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
    url('^open-ended/show/(?P<topic_slug>[-a-zA-Z]+)/$',
        GenerateFlashCardView.as_view(), name='next_flashcard'
    ),
    url('^open-ended/flip/(?P<slug>[-a-zA-Z]+)/$',
        FlipFlashCardView.as_view(), name='flashcard_flip'
    ),
    url('^open-ended/$', FlashCardListView.as_view(), name='flashcard_list'
    )
)

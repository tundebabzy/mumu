from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
#from django.views.decorators.cache import cache_page

from quizzer.views import (QuizSelectionView, GenerateQuizView, 
    GradeQuestionView, GenerateFlashCardView, FlipFlashCardView,
    FlashCardListView)

urlpatterns = patterns('',
    #url('^select/$', cache_page(60*15)(direct_to_template),
    #    {'template': 'select.html'}
    #),
    url('^select/$', QuizSelectionView.as_view(), name='quiz_selection'
    ),
    url('^grade/$', GradeQuestionView.as_view(), name='grader'
    ),
    url('^explanation/$', GradeQuestionView.as_view(), name='explanation'
    ),
    url('^pricing/$', TemplateView.as_view(template_name='pricing.html'),
        name='pricing'
    ),
    url('^how/$', TemplateView.as_view(template_name='how_it_works.html'),
        name='how_it_works'
    ),
    # This view also catches /subscribe/free/ so it is moved to the bottom
    url('^(?P<category>[a-zA-Z]+)/(?P<identifier>[a-zA-Z-]+)/$',
        GenerateQuizView.as_view(), name='next_question'
    ),
    url('^flashcard/show/(?P<topic_slug>[-a-zA-Z]+)/$',
        GenerateFlashCardView.as_view(), name='next_flashcard'
    ),
    url('^flashcard/flip/(?P<slug>[-a-zA-Z]+)/$',
        FlipFlashCardView.as_view(), name='flashcard_flip'
    ),
    url('^flashcard/$', FlashCardListView.as_view(), name='flashcard_list'
    )
)

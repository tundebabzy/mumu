from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView

from accounts.views import (PaymentHistoryView, FreeSessionView,
    StandardSessionView, StandardLiteSessionView, UpdateUserNamesView)

urlpatterns = patterns('',
    url('^history/$', PaymentHistoryView.as_view(),
        name='history'
    ),
    url('^subscribe/free/$', FreeSessionView.as_view(),
        name='free_session'
    ),
    url('subscribe/standard/$', StandardSessionView.as_view(),
        name='standard_session'
    ),
    url('subscribe/standard-lite/$', StandardLiteSessionView.as_view(),
        name='standard_lite_session'
    ),
    url('^change/personal/details/$', UpdateUserNamesView.as_view(),
        name='change_details'
    ),
)

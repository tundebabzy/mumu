from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView

from accounts.views import UpdateUserNamesView

urlpatterns = patterns('',
    url('^change/personal/details/$', UpdateUserNamesView.as_view(),
        name='change_details'
    ),
)

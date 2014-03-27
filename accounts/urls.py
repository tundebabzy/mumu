from django.conf.urls import patterns, url

from accounts.views import UpdateUserNamesView

urlpatterns = patterns('',
    url('^change/personal/details/$', UpdateUserNamesView.as_view(),
        name='change_details'
    ),
)

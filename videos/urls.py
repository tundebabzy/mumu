from django.conf.urls import patterns, url
from videos.views import ListVideos, DetailVideo

__author__ = 'tunde'

urlpatterns = patterns('',
                       url('^$', ListVideos.as_view(), name="video_list"),

                       url('^page/(?P<page>[0-9]+)/$', ListVideos.as_view(), name='video_list_paged'),

                       url('^(?P<pk>[0-9]+)/$', DetailVideo.as_view(), name='video'),
                       )

from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from mumublog.models import Article

__author__ = 'tunde'

urlpatterns = patterns('',
                       url('^$', ListView.as_view(paginate_by=2, http_method_names=['get'],
                                                  queryset=Article.objects.filter(approved=True),
                                                  template_name='bloglist.html'),
                           name='article_list'),

                       url('^page/(?P<page>[0-9]+)/$', ListView.as_view(
                           template_name='bloglist.html', queryset=Article.objects.filter(approved=True),
                           http_method_names=['get'], paginate_by=15),
                           name='article_list_paged'),

                       url('^(?P<slug>[a-zA-Z0-9-]+)/$', DetailView.as_view(template_name='article.html',
                                                              queryset=Article.objects.filter(approved=True),
                                                              http_method_names=['get']),
                           name='article'),
                       )
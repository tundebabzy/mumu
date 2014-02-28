from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, RedirectView
from registration.backends.default.views import ActivationView
from quizzer.views.backend import QuizzerRegistrationView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

class RedirectViewX(RedirectView):
    def get_redirect_url(self, **kwargs):
        download_url = '/static/downloads/%s' % kwargs['pdfname']
        return download_url

urlpatterns = patterns('',
    url('^downloads/(?P<pdfname>([a-zA-Z0-9-]+).pdf)$',
            RedirectViewX.as_view(), name='download_link'
    ),
    url('^downloads/$', TemplateView.as_view(template_name='downloads.html'), name='downloads'
    ),
    url('^favicon\.ico$',
            RedirectView.as_view(url='/static/img/favicon.ico'),
    ),
    url('^favicon\.png$',
            RedirectView.as_view(url='/static/img/favicon.png'),
    ),
    url('^media/favicon\.ico$',
            RedirectView.as_view(url='/static/img/favicon.ico'),
    ),
    url('^robots\.txt$',
            RedirectView.as_view(url='/static/robots.txt'),
    ),

    url('^blog/', include('mumublog.urls')),

    url('^practise/', include('quizzer.urls')),

    # Steal some django-registration url so I can shoe horn my backend
    url(r'^accounts/register/$', QuizzerRegistrationView.as_view(),
            name='registration_register'
    ),
    
    # This is the default however have to do this else the next url will
    # also catch /accounts/activate/complete/ which is meant for this url
    url(r'^accounts/activate/complete/$',
            TemplateView.as_view(template_name='registration/activation_complete.html'),
            name='registration_activation_complete'),

    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
            ActivationView.as_view(), name='registration_activate'
    ),
    url(r'^accounts/', include('registration.backends.default.urls')),
    
    url(r'^change/', include('accounts.urls')),
    
    url(r'^tinymce/', include('tinymce.urls')),

    url('^$', TemplateView.as_view(template_name='home.html'),
        name='home'
    ),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

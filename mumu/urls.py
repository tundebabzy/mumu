from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^quiz/', include('quizzer.urls')),

    # Steal one of django-registration url so I can shoe horn my backend
    url(r'^accounts/register/$', 'registration.views.register',
            {'backend': 'backends.QuizzerBackend',},
            name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    
    url(r'^change/', include('accounts.urls')),

    url(r'^grappelli/', include('grappelli.urls')),

    url('^$', TemplateView.as_view(template_name='home.html'),
        name='home'
    ),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

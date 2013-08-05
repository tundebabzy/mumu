from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/img/favicon.ico'}),

url('^favicon\.png$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/img/favicon.png'}),
                
    url('^media/favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/img/favicon.ico'}),

    url('^robots\.txt$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/robots.txt'}),        

    url('^quiz/', include('quizzer.urls')),

    # Steal some django-registration url so I can shoe horn my backend
    url(r'^accounts/register/$', 'registration.views.register',
            {'backend': 'backends.QuizzerBackend',},
            name='registration_register'),
    
    # This is the default however have to do this else the next url will
    # also catch /accounts/activate/complete/ which is meant for this url
    url(r'^accounts/activate/complete/$',
            direct_to_template,
            {'template': 'registration/activation_complete.html'},
            name='registration_activation_complete'),

    url(r'^accounts/activate/(?P<activation_key>\w+)/$', 'registration.views.activate',
           {'backend': 'backends.QuizzerBackend'},
           name='registration_activate'),

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

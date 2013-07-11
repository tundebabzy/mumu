from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages

from accounts.forms import UserNamesChangeForm

from lib.mixins import SubscriptionStatusMixin

class UpdateUserNamesView(UpdateView, SubscriptionStatusMixin):
    form_class = UserNamesChangeForm
    template_name = 'registration/info_change.html'
    success_url_view_name = 'quiz_selection'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 
                                        'Your account has been updated')
        if self.success_url_view_name:
            url = reverse(self.success_url_view_name)
        else:
            try:
                url = self.object.get_absolute_url()
            except:
                raise ImproperlyConfigured(
                        "No URL to redirect to. Either provide a url view name"
                        " or define a get_absolute_url method on the Model.")
        return url

    def get_object(self):
        """
        Simply returns the logged in user object
        """
        return self.request.user
        
    def get_context_data(self, **kwargs):
        context = super(UpdateUserNamesView, self).get_context_data(**kwargs)
        context.update({'status': self.account_status()})
        return context

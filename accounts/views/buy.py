from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import BaseCreateView
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.contrib import messages

from lib.mixins import SubscriptionStatusMixin
from utils.utils import FormError

from accounts.forms import PurchaseLevelForm, PurchasePaperForm
from quizzer.models import Payment

from utils.utils import get_last_payment

import datetime

class BaseBuySessionView(CreateView, SubscriptionStatusMixin):
    """
    Subclass to specify form_class
    """
    template_name = 'buy.html'
    success_url_view_name = 'quiz_selection'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseBuySessionView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Get Payment instance to add to ModelForm. First need to get the
        # expiry time for the user's last payment
        last_payment = get_last_payment(request)
        if last_payment:
            if last_payment.get_subscription_type() == 'Free':
                last_payment_expiry = last_payment.effective_time + datetime.timedelta(hours=24)
            else:
                last_payment_expiry = last_payment.effective_time + datetime.timedelta(days=30)
            self.object = Payment(user=request.user, effective_time=last_payment_expiry)
        else:
            self.object = Payment(user=request.user)
        # BaseCreateView which is next in the MRO will set self.object to None
        # again so we call the next in the MRO
        return super(BaseCreateView, self).post(request, *args, **kwargs)
        
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 
                                'The Transaction was succesful.')
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
    
    def get_context_data(self, **kwargs):
        context = super(BaseBuySessionView, self).get_context_data(**kwargs)
        context.update({'status': self.account_status(),})
        return context
        
    def get_form_kwargs(self):
        kwargs = super(BaseBuySessionView, self).get_form_kwargs()
        kwargs.update({'error_class': FormError })
        return kwargs


class FreeSessionView(BaseBuySessionView):
    form_class = PurchaseLevelForm

    def post(self, request, *args, **kwargs):
        # Check if the user has already had a free session in the past
        if request.user.payment_set.all().filter(has_used_free=True).exists():
            messages.add_message(request, messages.INFO, 
            'Unfortunately the transaction was aborted because you have already used your free session.')
            return HttpResponseRedirect(reverse('pricing'))
        # Get Payment instance to add to ModelForm
        self.object = Payment(user=request.user, has_used_free=True)
        # BaseCreateView which is the direct parent will set self.object to None
        # again so we call the next in the MRO
        return super(BaseCreateView, self).post(request, *args, **kwargs)
        
class StandardSessionView(BaseBuySessionView):
    form_class = PurchaseLevelForm
        
class StandardLiteSessionView(BaseBuySessionView):
    form_class = PurchasePaperForm

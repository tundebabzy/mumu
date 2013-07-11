from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from lib.mixins import SubscriptionStatusMixin

from quizzer.models import Payment

class PaymentHistoryView(ListView, SubscriptionStatusMixin):
    model = Payment
    template_name='history.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentHistoryView, self).dispatch(*args, **kwargs)
        
    def get_queryset(self):
        for obj in self.model.objects.all():
            print obj.time, obj.effective_time
        return self.model.objects.filter(user=self.request.user).order_by('-time')
        
    def get_context_data(self, **kwargs):
        print kwargs
        context = super(PaymentHistoryView, self).get_context_data(**kwargs)
        last_payment = context.get('object_list', None)
        if last_payment:
            context.update({'last_payment': last_payment[0].has_not_expired()})
        else:
            context.update({'last_payment': False })
        context.update({'status': self.account_status()})
        return context

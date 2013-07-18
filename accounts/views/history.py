from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from quizzer.models import Payment

class PaymentHistoryView(ListView):
    model = Payment
    template_name='history.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentHistoryView, self).dispatch(*args, **kwargs)
        
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-time')

from django.utils import timezone
import datetime

def sanitize(word):
    """
    This works by removing underscores from a supplied word
    and replacing with spaces instead. So new_example becomes
    new example. 
    """
    return str(word).strip().replace("_", " ")
    
def get_last_active_payment(request):
    user = request.user
    
    try:
        return user.payment_set.all().order_by('-effective_time').filter(effective_time__lte=timezone.now())[0]
    except IndexError:
        return None
    
def get_last_payment(request):
    user = request.user

    try:
        return user.payment_set.all().order_by('-effective_time')[0]
    except IndexError:
        return None

from django.utils import timezone
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe

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
    if user.is_anonymous():
        return None
    
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

class FormError(ErrorList):
    def __unicode__(self):
        return self.error_html()

    def error_html(self):
        if not self: return u''
        return mark_safe(u'%s' % ''.join([u'<small class="error">%s</small>' % e for e in self]))

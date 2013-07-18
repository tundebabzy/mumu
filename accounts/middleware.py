# "Pirated copy" of AuthenticationMiddleware

from django.utils.functional import SimpleLazyObject
from utils import utils

def get_last_active_payment(request):
    if not hasattr(request, '_cached_status'):
        request._cached_status = utils.get_last_active_payment(request)
    return request._cached_status

class MumuPaymentMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        request.status = SimpleLazyObject(lambda: get_last_active_payment(request))

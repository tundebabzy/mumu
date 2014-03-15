from django.http import HttpResponse
from django.views.generic import FormView

__author__ = 'tunde'


class NotifyMeView(FormView):
    def post(self, request, *args, **kwargs):
        email = self.request.POST.get('email')
        subject = self.request.POST.get('inform-me')
        token = self.request.POST.get('csrfmiddlewaretoken')
        form = self.form_class(**{'data': {'csrfmiddlewaretoken': token, 'email': email, 'level_name': subject}})

        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
            return HttpResponse('failed')
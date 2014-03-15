from django import forms
from django.contrib.auth.models import User
from accounts.models import NotifyMe


class UserNamesChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class NotifyMeForm(forms.ModelForm):
    class Meta:
        model = NotifyMe

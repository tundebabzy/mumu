from django import forms
from django.contrib.auth.models import User

from quizzer.models import Payment

class UserNamesChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
class PurchaseLevelForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['user', 'paper', 'time', 'has_used_free']
        
class PurchasePaperForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['user', 'level', 'time', 'has_used_free']

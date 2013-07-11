from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail
from quizzer.models import Question, Payment

attrs_dict = {'class': 'required'}

# Registration Form
class QuizzerForm(RegistrationFormUniqueEmail):
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
            label=_(u'I have read and agree to the Terms of Service'),
            error_messages={'required': _("You must agree to the terms to register")})
            
# Question Option Form
class OptionForm(forms.Form):
    options = forms.ModelChoiceField(queryset=None, widget=forms.widgets.RadioSelect,
                empty_label=None)

    # Add 1 extra arguments - `random_question`.
    # `random_question` is a Question instance or None
    # The extra argument is added as an instance variable.
    def __init__(self,random_question=None, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        self.random_question = random_question      
        self.fields['options'].queryset = self.random_question.option_set.all()

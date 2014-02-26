from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail
from lib.renderers import RadioFieldRendererWithoutUl
from quizzer.models import Question

attrs_dict = {'class': 'required'}

# Registration Form
class QuizzerForm(RegistrationFormUniqueEmail):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                label=_("E-mail"),
                error_messages={'required': _("This field is required"),
                                'invalid': _("Please enter a valid email address")})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                label=_("Password"),
                error_messages={'required': _("This field is required")})
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                label=_("Password (again)"),
                error_messages={'required': _("This field is required")})

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        err = "Enter the same thing into the two password fields" 
        if password1 and password2:
            if password1 != password2:
                self._errors['password1'] = self.error_class([err])
                self._errors['password2'] = self.error_class([err])
                
                del self.cleaned_data['password1']
                del self.cleaned_data['password2']
                
        return self.cleaned_data
          
# Question Option Form
class OptionForm(forms.Form):
    options = forms.ModelChoiceField(queryset=None, widget=forms.widgets.RadioSelect(**{'renderer': RadioFieldRendererWithoutUl}),
                empty_label=None)

    # Add 1 extra arguments - `random_question`.
    # `random_question` is a Question instance or None
    # The extra argument is added as an instance variable.
    def __init__(self,question=None, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        self.question = question      
        self.fields['options'].queryset = self.question.option_set.all()

    def as_normal(self):
        "Returns this form without those p or li or table tags."
        return self._html_output(
            normal_row = '%(errors)s%(field)s%(help_text)s',
            error_row = '%s',
            row_ender = '',
            help_text_html = ' <span class="helptext">%s</span>',
            errors_on_separate_row = False)

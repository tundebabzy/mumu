from django import forms
from django.http import Http404
from epiceditor.widgets import AdminEpicEditorWidget

from quizzer.models import Question, FlashCard


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        widgets = {
            'question_text': AdminEpicEditorWidget(),
            'code': forms.TextInput(),
            'explanation': AdminEpicEditorWidget(),
            'reference': AdminEpicEditorWidget(),
        }

    def save(self, request, commit):
        profile = request.user.get_profile()

        # The created_by field is hidden to Researchers. If instance.created_by
        # is empty, its most likely a Researcher in the Admin
        try:
            c = self.instance.created_by
        except:
            try:
                self.instance.created_by = profile.researcher_set.all()[0]
            except:
                # User is not a Researcher
                raise Http404
            

        # self.instance.approved is False by default. Researchers are not
        # shown the approved check button so if instance.approved
        # becomes False then it means an Editor is using the site
        if self.instance.approved:
            try:
                editor = profile.editor_set.all()[0]
            except:
                raise Http404
        return super(QuestionForm, self).save(commit=False)

class FlashCardForm(QuestionForm):
    class Meta:
        model = FlashCard
        widgets = {
            'question_text': AdminEpicEditorWidget(),
            'code': forms.TextInput(),
            'explanation': AdminEpicEditorWidget(),
            'reference': AdminEpicEditorWidget(),
        }

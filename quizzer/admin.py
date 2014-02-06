from django.contrib import admin
from quizzer.models import *

# Customised ModelAdmin classes
class FilteredModelAdmin(admin.ModelAdmin):
    """
    Extends its parent by filtering returned queryset with its
    `created_by` attribute
    """
    def get_readonly_fields(self, request, obj=None):
        """
        Hook for specifying custom readonly fields.
        """
        if self.readonly_fields:
            if request.user.is_superuser or 'Editors' not in request.user.groups.values_list('name', flat=True):
                self.readonly_fields = ()
        return self.readonly_fields
        
    def queryset(self, request):
        queryset = super(FilteredModelAdmin, self).queryset(request)
        if not request.user.is_superuser and not 'Editors' in request.user.groups.values_list('name', flat=True):
            if self.has_change_permission(request):
                queryset = queryset.filter(created_by__staff__user = request.user)
        return queryset

    def save_form(self, request, form, change):
        """
        Unlike the default, it takes an extra argument - `request`
        """
        return form.save(request, commit=False)

    def get_form(self, request, obj=None, **kwargs):
        """
        Does a little magic thus the `exclude` attribute of
        FilteredModelAdmin is ignored if the User is a super user or
        is a member of the Editor group
        """
        if self.exclude:
            if request.user.is_superuser or 'Editors' in request.user.groups.values_list('name', flat=True):
                if 'slug' in self.exclude:
                    self.exclude = list(['slug'])
                else:
                    self.exclude = None
        return super(FilteredModelAdmin, self).get_form(request, obj, **kwargs)
            

class ExamAdmin(admin.ModelAdmin):
    fields = ['name']
admin.site.register(Exam, ExamAdmin)

class LevelAdmin(admin.ModelAdmin):
    fields = ['name']
admin.site.register(Level, LevelAdmin)

class PaperAdmin(admin.ModelAdmin):
    fields = ['name']
admin.site.register(Paper, PaperAdmin)

class TopicAdmin(admin.ModelAdmin):
    fields = ['name']
admin.site.register(Topic, TopicAdmin)

admin.site.register(Payment)
#admin.site.register(Login)
#admin.site.register(AnswerLogs)
admin.site.register(Link)
#admin.site.register(EditorComment)
#admin.site.register(QuestionReference)

class OptionInline(admin.StackedInline):
    model = Option
    extra = 0
    
class OptionExplanationInline(admin.StackedInline):
    from adminform import adminforms
    model = OptionExplanation
    form = adminforms.OptionExplanationForm
    extra = 0
    
class LinkInline(admin.StackedInline):
    model = Link
    extra = 0
    
class EditorCommentAdmin(admin.StackedInline):
    model = EditorComment
    extra = 0

class QuestionReferenceAdmin(admin.StackedInline):
    model = QuestionReference
    extra = 0

class QuestionAdmin(FilteredModelAdmin):
    from adminform import adminforms
    inlines = [OptionInline, OptionExplanationInline, LinkInline, QuestionReferenceAdmin, EditorCommentAdmin]
    list_display = ['text', 'approved']
    exclude = ('created_by', 'approved', 'approved_by')
    form = adminforms.QuestionForm
    readonly_fields = ('created_by', 'text')
    search_fields = ['text']
admin.site.register(Question, QuestionAdmin)

class FlashCardAdmin(FilteredModelAdmin):
    from adminform import adminforms
    exclude = ['slug', 'created_by', 'approved', 'approved_by']
    readonly_fields = ('created_by', 'text')
    search_fields = ['text']
    form = adminforms.FlashCardForm
admin.site.register(FlashCard, FlashCardAdmin)
admin.site.register(Code)

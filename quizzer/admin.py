from django.contrib import admin
from quizzer.models import *

class FilteredModelAdmin(admin.ModelAdmin):
    """
    Extends its parent by filtering returned queryset with its
    `created_by` attribute
    """
    def queryset(self, request):
        """
        Adds a filter constraint to queryset before executing the query
        when the User object is not a superuser or part of the editor
        group.
        """
        queryset = super(FilteredModelAdmin, self).queryset(request)
        if not request.user.is_superuser and not 'Editors' in request.user.groups.values_list('name', flat=True):
            if self.has_change_permission(request):
                queryset = queryset.filter(created_by__staff__user = request.user)
        return queryset

    def save_form(self, request, form, change):
        """
        Unlike the default, it takes an extra argument - `request`.

        The `request` is later passed on to the `get_form` method
        """
        return form.save(request, commit=False)

    def get_form(self, request, obj=None, **kwargs):
        """
        The `Request` object received from `save_form` method is used to
        determine if the `User` object is a superuser or belongs to the
        'Editor' `Group`.
        
        If the `User` satisfies the condition, the exclude attribute is
        ignored.
        """
        if self.exclude:
            if request.user.is_superuser or 'Editors' in request.user.groups.values_list('name', flat=True):
                self.exclude = None
        return super(FilteredModelAdmin, self).get_form(request, obj, **kwargs)

class OptionInline(admin.StackedInline):
    model = Option
    extra = 0

class LinkInline(admin.StackedInline):
    model = Link
    extra = 0

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class QuestionAdmin(FilteredModelAdmin):
    from adminform import adminforms
    inlines = [OptionInline, LinkInline, CommentInline]
    list_display = ['question_text', 'approved']
    exclude = ('created_by', 'approved', 'approved_by')
    form = adminforms.QuestionForm
    search_fields = ['question_text']

class FlashCardAdmin(FilteredModelAdmin):
    from adminform import adminforms
    list_display = ['question_text', 'approved']
    exclude = ('created_by', 'approved', 'approved_by')
    form = adminforms.FlashCardForm
    search_fields = ['question_text']

admin.site.register(Code)
admin.site.register(FlashCard, FlashCardAdmin)
admin.site.register(Question, QuestionAdmin)
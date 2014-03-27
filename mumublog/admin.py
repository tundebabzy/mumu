from django.contrib import admin
from django.db import models
from epiceditor.widgets import AdminEpicEditorWidget
from mumublog.models import Article

__author__ = 'tunde'

class ArticleAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    formfield_overrides = {
        models.TextField: {'widget': AdminEpicEditorWidget}
    }

admin.site.register(Article, ArticleAdmin)
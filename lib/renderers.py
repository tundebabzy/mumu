from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.html import format_html, format_html_join

__author__ = 'tunde'

# Put any widget renderer code here

@python_2_unicode_compatible
class RadioFieldRendererWithoutUl(RadioFieldRenderer):
    def render(self):
        """Unlike the Parent, it renders without the `ul` tags"""
        return format_html('{0}\n',
                           format_html_join('\n', '{0}',
                                            [(force_text(w),) for w in self]
                                            ))
__author__ = 'tunde'

from django import template
import markdown

register = template.Library()

@register.filter
def convert_markdown(text):
    """
    Ideally, there should be sanitizers but considering the fact that the admin is going to be open to only trusted
    people, i'm going to give the benefit of a doubt because bleach is not fast.
    """
    return markdown.markdown(text, extensions=['tables'])


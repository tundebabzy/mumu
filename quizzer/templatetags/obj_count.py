from django import template
from django.contrib.contenttypes.models import ContentType

from quizzer.models import FlashCard

register = template.Library()

class CountNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def get_object_from_node(self, context):
        return context.render_context[self]['obj'].resolve(context)

    def render(self, context):
        if not self in context.render_context:
            # For the first time the node is rendered in the template
            context.render_context[self] = {'obj': self.obj}
        try:
            return self.get_count(context)
        except:
            return ''

    def get_count(self, context):
        obj = self.get_object_from_node(context)
        return FlashCard.objects.filter(topic=obj).count()

@register.tag(name="obj_count")
def count(parser, token):
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('tag takes exactly one argument')
    return CountNode(obj)

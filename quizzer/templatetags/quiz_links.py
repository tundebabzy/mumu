from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django import template

from quizzer.models import FlashCard, Question
from lib.decoder import ExamCodeDecoder


__author__ = 'tunde'

register = template.Library()
decoder = ExamCodeDecoder()

def trim_to_level_code(the_list):
    return [value[1:3] for value in the_list]


def trim_to_paper_code(the_list):
    return [value[3:5] for value in the_list]

def trim_to_topic_code(the_list):
    return [value[5:] for value in the_list]


@register.tag(name="open_ended_links")
def get_categories(parser, token):
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'Tag takes no argument'
        )
    return NavigationNode(FlashCard, 'next_flashcard')


@register.tag(name="multiple_choice_links")
def get_categories(parser, token):
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'Tag takes no argument'
        )
    return NavigationNode(Question, 'next_question')


class NavigationNode(template.Node):
    def __init__(self, model, view_name):
        self.model = model
        self.view_name = view_name

    def render(self, context):
        if not self in context.render_context:
            context.render_context[self] = {'key': None, 'model': self.model, 'view_name': self.view_name}
        return self.get_html_code(context)

    def get_html_code(self, context):
        """
        Returns the HTML to be rendered in the template
        :rtype : Unicode
        """
        html = self.build_html(context)
        return html

    def build_html(self, context):
        """
        Create the HTML to be rendered in the template dynamically
        :rtype : Unicode
        """
        codes = self.get_values_list(context.render_context[self]['model'], context)
        html_for_papers = '<li><label>Paper</label></li>'
        html_for_topics = '<li><label>Topics</label></li>'
        paper_codes = list(set(trim_to_paper_code(codes)))
        topic_codes = list(set(trim_to_topic_code(codes)))

        for code in sorted(paper_codes):
            paper_name = decoder.sub_code_to_text(code, 'paper')
            html = '''<li><a href="%s">%s</a></li>''' % (
                reverse(context.render_context[self]['view_name'],
                        kwargs={'category': 'paper', 'identifier': slugify(paper_name), 'code': code},
                ),
                paper_name
            )
            html_for_papers += html

        for code in sorted(topic_codes):
            topic_name = decoder.sub_code_to_text(code, 'topic')
            html2 = '''<li><a href="%s">%s</a></li>''' % (
                reverse(context.render_context[self]['view_name'],
                        kwargs={'category': 'topic', 'identifier': slugify(topic_name), 'code': code},
                        ),
                topic_name
            )
            html_for_topics += html2

        return html_for_papers+html_for_topics


    def get_values_list(self, model, context, key='key'):
        """
        Use this to do a database query for the model argument supplied.
        The method retrieves distinct records based on the supplied codes
        :param model: model object to be queried
        :param key: Any string. To be used as a key for the context
        :param context: Context object
        :rtype : list
        """
        if not context.render_context[self][key]:
            context.render_context[self][key] = list(
                model.objects.order_by('code').distinct('code').values_list('code__code', flat=True))
        return context.render_context[self][key]

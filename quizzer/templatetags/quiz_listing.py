from django import template
from django.template.defaultfilters import slugify

from quizzer.models import Question, FlashCard
from lib.decoder import ExamCodeDecoder


register = template.Library()
decoder = ExamCodeDecoder()


class NavigationNode(template.Node):
    model = Question

    def __init__(self, domain):
        self.domain = template.Variable(domain)  # This should be a simple string

    def _gen_html(self, html_h_tag, category_type, category_desc, code,
                  context, count=None):
        return u"""
        <%s><a href="http://%s/practise/multiple-choice/%s/%s/random/%s/">%s <span class=" round label">%s</span></a><%s>
        """ % (html_h_tag,
               self.get_domain(context), category_type,
               slugify(category_desc),
               decoder.get_category_code(code, category_type),
               category_desc, count or 'Available', html_h_tag
        )

    def _open_div(self, heading):
        return u"""
            <div class="panel">
                <h5 class="subheader">%s</h5>
                """ % heading

    def _close_div(self):
        return u'</div>'

    def get_domain(self, context):
        return context.render_context[self]['domain'].resolve(context)

    def get_queryset(self):
        return Question.objects.order_by('code').distinct('code').values_list('code__code', flat=True)

    def make_html(self, context):
        queryset = self.get_queryset()
        category_html_level, category_html_paper, category_html_topic = '', '', ''
        temp_level, temp_paper = [], []

        for code in queryset:
            level = decoder.translate_code(code, 'level')
            paper = decoder.translate_code(code, 'paper')
            topic = decoder.translate_code(code, 'topic')

            if not level in temp_level:
                category_html_level += self._gen_html('h5', 'level', level, code, context)
                temp_level.append(level)
            if not paper in temp_paper:
                category_html_paper += self._gen_html('h5', 'paper', paper, code, context)
                temp_paper.append(paper)
            # Because topic is definitely not going to have duplicates
            count = self.model.objects.filter(code__code=code).count()
            category_html_topic += self._gen_html('h5', 'topic', topic, code, context, count)

        category_html_level = self._open_div('LEVEL') + category_html_level + self._close_div()
        category_html_paper = self._open_div('PAPER') + category_html_paper + self._close_div()
        category_html_topic = self._open_div('TOPIC') + category_html_topic + self._close_div()

        html = category_html_level + category_html_paper + category_html_topic
        return html

    def render(self, context):
        if not self in context.render_context:
            # For the first time the node is rendered in the template
            context.render_context[self] = {'domain': self.domain}
        #        return self.make_html(context)
        try:
            return self.make_html(context)
        except:
            return ''


class NavigationNodeF(NavigationNode):
    model = FlashCard

    def _gen_html(self, html_h_tag, category_type, category_desc, code,
                  context, count=None):
        return u"""
        <%s><a href="http://%s/practise/open-ended/%s/%s/random/%s/">%s <span class="round label">%s</span></a><%s>
        """ % (html_h_tag,
               self.get_domain(context), category_type,
               slugify(category_desc),
               decoder.get_category_code(code, category_type),
               category_desc, count or 'Available', html_h_tag
        )

    def get_queryset(self):
        return FlashCard.objects.order_by('code').distinct('code').values_list('code__code', flat=True)


@register.tag(name="categories")
def get_categories(parser, token):
    try:
        tag_name, domain = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'Tag takes one argument which is a domain name'
        )
    return NavigationNode(domain)


@register.tag(name="categoriesf")
def get_categories(parser, token):
    try:
        tag_name, domain = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'Tag takes one argument which is a domain name'
        )
    return NavigationNodeF(domain)

from django import template
from django.contrib.contenttypes.models import ContentType

from quizzer.models import Question

register = template.Library()

class NavigationNode(template.Node):
    def __init__(self, user_obj, payment_obj):
        self.user_obj = template.Variable(user_obj)
        self.payment_obj = template.Variable(payment_obj)
        
    def get_user_from_node(self, context):
        return context.render_context[self]['user'].resolve(context)
        
    def get_user_last_payment(self, context):
        return context.render_context[self]['payment_obj'].resolve(context)

    def _gen_html(self, tag_type, level_or_paper, label, obj):
        model_ct = ContentType.objects.get_for_model(obj)
        model_name = model_ct.model_class()
        if label == 'level':
            num = model_name.objects.filter(level=obj.level).count()
        elif label == 'paper':
            num = model_name.objects.filter(level=obj.level, paper=obj.paper).count()
        elif label == 'topic':
            num = model_name.objects.filter(level=obj.level, paper=obj.paper, topic=obj.topic).count()
        return u"""
                <%s><a href="%s">%s</a> <span class="label round">%s</span></%s>
        """ %(tag_type, level_or_paper.get_absolute_url(), level_or_paper, num,
              tag_type)
        
    def _open_div(self, marker):
        return u"""
            <div class="panel">
                <h5 class="subheader">%s</h5>
                """ % marker
        
    def _close_div(self):
        return u'</div>'
        
    def _error_html(self):
        return u"""
        <div class="panel">
            <h5 class="subheader">ACCESS DENIED</h5>
            <h6>This message normally appears when your subscription has 
            expired or if you don't have a subscription. If none of these
            apply to you, please contact us immediately and we will fix
            the issue for you.
            """

    def make_html(self, context):
        user = self.get_user_from_node(context)
        distinct_quests = Question.objects.select_related().order_by('topic').distinct('topic')
        level_html, paper_html, topic_html = '', '', ''
        temp_level, temp_paper = [], []
                        
        for obj in distinct_quests:
            if not obj.level in temp_level:
                level_html += self._gen_html('h5', obj.level, 'level', obj)
                temp_level.append(obj.level)
            if not obj.paper in temp_paper:
                paper_html += self._gen_html('h5', obj.paper, 'paper', obj)
                temp_paper.append(obj.paper)
            topic_html += self._gen_html('h5', obj.topic, 'topic', obj)
        
        level_html = self._open_div('LEVEL') + level_html + self._close_div()
        paper_html = self._open_div('PAPER') + paper_html + self._close_div()
        topic_html = self._open_div('TOPIC') + topic_html + self._close_div()

        html = level_html + paper_html + topic_html
        return html

    def render(self, context):
        if not self in context.render_context:
            # For the first time the node is rendered in the template
            context.render_context[self] = {
                'user': self.user_obj, 'payment_obj': self.payment_obj
            }
        try:
            return self.make_html(context)
        except:
            return ''

@register.tag(name="quiz_listing")
def get_categories(parser, token):
    try:
        tag_name, user_obj, payment_obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('tag takes two arguments')
    return NavigationNode(user_obj, payment_obj)

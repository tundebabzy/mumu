from django import template
from django.utils.timezone import make_aware, get_current_timezone

from quizzer.models import Question

import datetime

register = template.Library()

class NavigationNode(template.Node):
    def __init__(self, user_obj, payment_obj):
        self.user_obj = template.Variable(user_obj)
        self.payment_obj = template.Variable(payment_obj)
        
    def get_user_from_node(self, context):
        return context.render_context[self]['user'].resolve(context)
        
    def get_user_last_payment(self, context):
        return context.render_context[self]['payment_obj'].resolve(context)

    def _gen_html(self, tag_type, obj):
        return u"""
                <%s><a href="%s">%s</a></%s>
        """ %(tag_type, obj.get_absolute_url(), obj, tag_type)
        
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
        #last_payment = self.get_user_last_payment(context)
        distinct_quests = Question.objects.select_related().order_by('topic').distinct('topic')

#        if not user.is_staff:
#            if last_payment is None:
#                return self._error_html()
#            elif not last_payment is None and not last_payment.has_not_expired():
#                return self._error_html()
#            if last_payment.get_category_paid_for() == 'level':
#                distinct_quests = distinct_quests.filter(level=last_payment.level)
#            elif last_payment.get_category_paid_for() == 'paper':
#                distinct_quests = distinct_quests.filter(paper=last_payment.paper)

        level_html, paper_html, topic_html = '', '', ''
        temp_level, temp_paper = [], []
                        
        for obj in distinct_quests:
#            if user.is_staff or last_payment.get_category_paid_for() == 'level':
            if not obj.level in temp_level:
                level_html += self._gen_html('h3', obj.level)
                temp_level.append(obj.level)
            if not obj.paper in temp_paper:
                paper_html += self._gen_html('h4', obj.paper)
                temp_paper.append(obj.paper)
            topic_html += self._gen_html('h5', obj.topic)
        
#        if user.is_staff or last_payment.get_category_paid_for() == 'level':
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
        raise template.TemplateSyntaxError('tag takes exactly one argument')
    return NavigationNode(user_obj, payment_obj)

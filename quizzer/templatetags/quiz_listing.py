from django import template
from django.utils.timezone import make_aware, get_current_timezone

from quizzer.models import Question

import datetime

register = template.Library()

class NavigationNode(template.Node):
    def __init__(self, user_obj):
        self.user_obj = template.Variable(user_obj)
        
    def get_user_from_node(self, context):
        user = context.render_context[self].resolve(context)
        return user
        
    def get_user_last_payment(self, user):
        try:
            tz = get_current_timezone()
            now = datetime.datetime.now()
            last_payment = user.payment_set.all().order_by('-effective_time').filter(effective_time__lte=make_aware(now, tz))[0]
        except IndexError:
            return None
        return last_payment
        
    def _gen_html(self, tag_type, obj):
        return u"""
                <%s><a href="%s">%s</a><%s>
        """ %(tag_type, obj.get_absolute_url(), obj, tag_type)
        
    def _open_div(self, marker):
        return u"""
            <div class="panel">
                <h5 class="subheader">%s</h5>
                """ % marker
        
    def _close_div(self):
        return u'</div>'

    def make_html(self, context):
        user = self.get_user_from_node(context)
        last_payment = self.get_user_last_payment(user)
        distinct_quests = Question.objects.select_related().distinct('topic')
        html = ''
        
        if last_payment:
            if last_payment.get_category_paid_for() == 'level':
                html += self._open_div('LEVEL')
                html += self._gen_html('h2', last_payment.level)
            elif last_payment.get_category_paid_for() == 'paper':
                html += self._open_div('PAPER')
                html += self._gen_html('h3', last_payment.paper)
            html += self._close_div()
            html += self._open_div('PAPERS')
            if last_payment.get_category_paid_for() == 'level':
                distinct_quests = distinct_quests.filter(level=last_payment.level)
                for obj in distinct_quests:
                    html += self._gen_html('h3', obj.paper)
            html += self._close_div()
            html += self._open_div('TOPICS')
            for obj in distinct_quests:
                html += self._gen_html('h4', obj.topic)
            html += self._close_div()
            return html

    def render(self, context):
        if not self in context.render_context:
            # For the first time the node is rendered in the template
            context.render_context[self] = self.user_obj
        try:
            return self.make_html(context)
        except:
            return ''

@register.tag(name="quiz_listing")
def get_categories(parser, token):
    try:
        tag_name, user_obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('tag takes exactly one argument')
    return NavigationNode(user_obj)

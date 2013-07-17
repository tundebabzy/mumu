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
        last_payment = self.get_user_last_payment(user)
        
        if not user.is_staff and last_payment is None:
            return self._error_html()
        elif not last_payment is None and not last_payment.has_not_expired():
            return self._error_html()
            
        distinct_quests = Question.objects.select_related().order_by('topic').distinct('topic')
        html = ''
        
        for category in ['LEVEL', 'PAPER', 'TOPIC']:
            temp = []
            if not last_payment is None and last_payment.get_category_paid_for() == 'paper':
                distinct_quests = distinct_quests.order_by('level', 'paper').distinct('paper').filter(paper=last_payment.paper)
                continue
            if not last_payment is None and last_payment.get_category_paid_for() == 'level':
                distinct_quests = distinct_quests.order_by('level', 'paper').distinct('level', 'paper').filter(level=last_payment.level)
            html += self._open_div(category)
            for obj in distinct_quests:
                temp2 = None
                if category == 'LEVEL':
                    if obj.level in temp:
                        continue
                    else:
                        temp.append(obj.level)
                    html += self._gen_html('h4', obj.level)
                elif category == 'PAPER':
                    if obj.paper in temp:
                        continue
                    else:
                        temp.append(obj.paper)
                    html += self._gen_html('h4', obj.paper)
                elif category == 'TOPIC': 
                    if obj.topic in temp:
                        continue
                    else:
                        temp2 = obj.topic
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

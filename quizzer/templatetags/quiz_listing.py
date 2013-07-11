from django import template
from django.utils.timezone import make_aware, get_current_timezone

from treelib import Tree

from quizzer.models import Question

from utils.utils import sanitize

import time
import datetime

register = template.Library()

class NavigationNode(template.Node):
    def __init__(self, user_obj):
        self.user_obj = template.Variable(user_obj)

    # FIXME: make tree by introspecting the Payment object
#    def _make_node(tree, category, url, parent=None):
#        if not tree.get_node(category):
#            tree.create_node(url, category, parent)
            
#    def _make_tree(self, context):
#        user = self.user_obj.resolve(context)
#        try:
#            tz = get_current_timezone()
#            now = datetime.datetime.now()
#            last_payment = user.payment_set.all().order_by('-effective_time').filter(effective_time__lte=make_aware(now, tz))[0]
#        except IndexError:
#            return None
            
#        included = ['level_id', 'paper_id']
            
#        if last_payment.get_category_paid_for() == 'level':
#            categories = Question.objects.select_related().filter(level=last_payment.level).distinct('topic')
#        elif last_payment.get_category_paid_for() == 'paper':
#            categories = Question.objects.select_related().filter(paper=last_payment.paper).distinct('topic')
#        elif user.is_staf:
#            included.append('exam_id')
#            categories = Question.objects.select_related().distinct('topic')
        
#        for obj in categories:
#            prev = None
#            for f in obj._meta.fields:
#                if not f.attname in included:
#                    continue
#                print f.rel.field_name

#                if prev:
#                    parent = prev
#                else:
#                    prev = f.rel.to
                #self._make_node(context.render_context[self], f.rel.to.get_absolute_url(), parent)
                

    def _make_tree(self, context):
        def _add_level_as_root(obj):
            if not context.render_context[self].get_node(obj.level):
                context.render_context[self].create_node(obj.level.get_absolute_url(), obj.level)
            if not context.render_context[self].get_node(obj.paper):
                context.render_context[self].create_node(obj.paper.get_absolute_url(), obj.paper, parent=obj.level)
            if not context.render_context[self].get_node(obj.topic):
                context.render_context[self].create_node(obj.topic.get_absolute_url(), obj.topic, parent=obj.paper)

        def _add_paper_as_root(obj):
            if not context.render_context[self].get_node(obj.paper):
                context.render_context[self].create_node(obj.paper.get_absolute_url(), obj.paper)
            if not context.render_context[self].get_node(obj.topic):
                context.render_context[self].create_node(obj.topic.get_absolute_url(), obj.topic, parent=obj.paper)
                
        user = self.user_obj.resolve(context)
        
        try:
            tz = get_current_timezone()
            now = datetime.datetime.now()
            last_payment = user.payment_set.all().order_by('-effective_time').filter(effective_time__lte=make_aware(now, tz))[0]
        except IndexError:
            return None

        if last_payment.get_category_paid_for() == 'level':
            categories = Question.objects.select_related().filter(level=last_payment.level).distinct('topic')
            if categories:
                map(_add_level_as_root, categories)
                
        elif last_payment.get_category_paid_for() == 'paper':
            categories = Question.objects.select_related().filter(paper=last_payment.paper).distinct('topic')
            if categories:
                map(_add_paper_as_root, categories)

    def _make_html(self, context):
        # =====================================================================
        # STARTING VARIABLES
        # =====================================================================
        self._make_tree(context)
        tree = context.render_context[self]
        root = tree.root
        html = u''
        root_node = tree.get_node(root)
        # =====================================================================
        # =====================================================================

        # Here are HTML code helpers to keep readability within sanity limits.
        # =====================================================================
        def _get_h2(root_node):
            return u'<h2><a href="%s">%s</a></h2><hr />' % (root_node.tag, 
                                        sanitize(root_node.identifier))
                                        
        def _get_h3(child_node):
            return u'<h3><a href="%s">%s</a></h3><hr />' % (child_node.tag, 
                                        sanitize(child_node.identifier))
                                        
        def _get_dt(grandchild_node):
            return u'<dt><a href="%s">%s</a></dt>' % (grandchild_node.tag,
                                     sanitize(grandchild_node.identifier))
                                     
        def _get_dd(greatchild_node):
            return u'<dd><a href="%s">%s</a></dd>' % (greatchild_node.tag,
                                                 sanitize(greatchild))
                                                 
        def _get_dl_tag(dt_tag, dd_tag):
            return u'<dl>%s%s</dl>' % (dt, dd_tag)
            
        def _get_dd_tag(dd_list):
            return ''.join(dd_list)
        # =====================================================================
        # =====================================================================
                                                 
        h2 = _get_h2(root_node)
        
        for child in root_node.fpointer:
            child_node = tree.get_node(child)
            h3 = _get_h3(child_node)
            html = html + h3
            
            for grandchild in child_node.fpointer:
                dd = list()
                grandchild_node = tree.get_node(grandchild)
                dt = _get_dt(grandchild_node)
                
                for greatchild in grandchild_node.fpointer:
                    greatchild_node = tree.get_node(greatchild)
                    dd.append(_get_dd(greatchild_node))
                    
                dd_tag = _get_dd_tag(dd)
                dl_tag = _get_dl_tag(dt, dd_tag)
                html = html + dl_tag
                
        return html 

    def render(self, context):
        if not self in context.render_context:
            # For the first time the node is rendered in the template
            context.render_context[self] = Tree()
        try:
            return self._make_html(context)
        except:
            return ''

@register.tag(name="quiz_listing")
def get_categories(parser, token):
    try:
        tag_name, user_obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('tag takes exactly one argument')
    return NavigationNode(user_obj)

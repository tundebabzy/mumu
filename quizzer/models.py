from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.html import strip_tags

from accounts.models import Researcher, Editor, QuizzerProfile
from db import mixin

import datetime

class Exam(models.Model):
    """
    An exam.
    """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=80)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # Means not already existing
            self.slug = slugify(self.name)
        super(Exam, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('next_question', (), {
                'category': 'exam',
                'identifier': self.slug
                })

class Level(models.Model):
    """
    An exam level.
    """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=80)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # Means not already existing
            self.slug = slugify(self.name)
        super(Level, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('next_question', (), {
                'category': 'level',
                'identifier': self.slug
                })
        
class Paper(models.Model):
    """
    An exam level paper.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=80)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # Means not already existing
            self.slug = slugify(self.name)
        super(Paper, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('next_question', (), {
                'category': 'paper',
                'identifier': self.slug
                })
        
class Topic(models.Model):
    """
    An exam level paper topic.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=150)

    def save(self, *args, **kwargs):
        if not self.id:
            # Means not already existing
            self.slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('next_question', (), {
                'category': 'topic',
                'identifier': self.slug
                })
        
class Question(models.Model, mixin.ModelDiffMixin):
    exam = models.ForeignKey(Exam)
    level = models.ForeignKey(Level)
    paper = models.ForeignKey(Paper)
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    created_by = models.ForeignKey(Researcher)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField()
    approved_by = models.ForeignKey(Editor, blank=True, null=True)

    def __unicode__(self):
        return '%s' % strip_tags(self.text)
        
class FlashCard(models.Model, mixin.ModelDiffMixin):
    exam = models.ForeignKey(Exam)
    level = models.ForeignKey(Level)
    paper = models.ForeignKey(Paper)
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    answer = models.TextField()
    created_by = models.ForeignKey(Researcher)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField()
    approved_by = models.ForeignKey(Editor, blank=True, null=True)
    slug = models.SlugField(max_length=300)
    
    class Meta:
        verbose_name = 'Flash Card'

    def __unicode__(self):
        return self.text
        
    def save(self, *args, **kwargs):
        if not self.id:
            # Means not already existing
            self.slug = slugify(self.text)
        super(FlashCard, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('next_flashcard', (), {
                'topic_slug': self.topic.slug,
                #'slug': self.slug
                })

class Option(models.Model):
    text = models.CharField(max_length=90)
    question = models.ForeignKey(Question)
    is_true = models.BooleanField()

    def __unicode__(self):
        return self.text

class OptionExplanation(models.Model):
    explanation = models.TextField()
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return '%s' % strip_tags(self.explanation)

class QuestionReference(models.Model):
    source = models.CharField(max_length=100)
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return self.source 

class EditorComment(models.Model, mixin.ModelDiffMixin):
    comment = models.TextField()
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return '%s' % self.comment

class Link(models.Model):
    link = models.URLField()
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return '%s' % self.link

class Payment(models.Model):
    """
    Contains the payment information
    """
    tz = timezone.get_current_timezone()
    user = models.ForeignKey(User)
    level = models.ForeignKey(Level, blank=True, null=True)
    paper = models.ForeignKey(Paper, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now, editable=False)
    effective_time = models.DateTimeField(default=timezone.now, editable=False)
    has_used_free = models.BooleanField(default=False)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.level and not self.paper:
            raise ValidationError('You have not made a selection')
    
    def __unicode__(self):
        return '%s: %s' %(self.get_subscription_type(), self.get_status())
        
    def get_active_period(self, key):
        period = {
            'Free': datetime.timedelta(hours=24),
            'Standard': datetime.timedelta(days=30),
            'Standard Lite': datetime.timedelta(days=30),
        }
        return period.get(key, None)

    def get_subscription(self):
        if self.has_used_free:
            return ('free', self.has_used_free)
        if  self.level:
            return ('level', self.level)
        if self.paper:
            return ('paper', self.paper)

    def get_expiry_date(self):
        return self.effective_time + self.get_active_period(self.get_subscription_type())

    def has_not_expired(self):
        return self.get_expiry_date() >= timezone.now()

    def get_payment_date(self):
        return self.time.strftime("%A, %d. %B %Y %I:%M%p")
        
    def get_category_paid_for(self):
        if self.level: return 'level'
        elif self.paper: return 'paper'
        
    def get_subscription_type(self):
        if self.has_used_free:
            return 'Free'
        if self.level:
            return 'Standard'
        if self.paper:
            return 'Standard Lite'
        return None
            
    def get_status(self):
        if self.has_not_expired():
            return 'Active'
        else:
            return 'Expired'

class Login(models.Model):
    user = models.ForeignKey(User)
    session_key = models.CharField(max_length=40)
    http_user_agent = models.CharField(max_length=400, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __unicode__(self):
        return '%s: %s' % (self.user, self.session_key)

class AnswerLogs(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Option)
    time = models.DateTimeField(auto_now_add=True)
              
# SIGNAL TRIGGERED FUNCTIONS
@receiver(post_save, sender=EditorComment)
def correction_notification(sender, **kwargs):
    editor_comment = kwargs['instance']
    if editor_comment.has_changed:
        question = editor_comment.question

        subject = "mumu.com.ng: Your Editor Made A Comment About Your Question Entry"
        from_email = settings.MAILER_USER
        to_email = question.created_by.staff.user.email
        message = """
        Hi,\n Please have a look at the comment I made concerning your question entry: %s and perform the recommended action.\n My comment was : %s.\n Thanks.\n mumu.com.ng
        """ %(question.id, editor_comment)
        __password = settings.MAILER_USER_PASSWORD
        
        try:
            send_mail(subject, message, from_email, [to_email], 
                fail_silently=False, auth_user=from_email,
                auth_password=__password)
        except BadHeaderError:
            return HttpResponse('Invalid header found')

@receiver(post_save, sender=Question)
def approval_notification(sender, **kwargs):
    question = kwargs['instance']
    if question.has_changed:
        if 'approved' in question.changed_fields:
            subject = 'mumu.com.ng: Approval notice'
            from_email = settings.MAILER_USER
            to_email = question.created_by.staff.user.email
            message = """Hi,\n the approval status of your question entry #%s has changed. Please check the admin to check if your entry has been approved.\nThanks.\nmumu.com.ng""" % question.id
            __password = settings.MAILER_USER_PASSWORD

            try:
                send_mail(subject, message, from_email, [to_email],
                    fail_silently=False, auth_user=from_email,
                    auth_password=__password)
            except BadHeaderError:
                return HttpResponse('Invalid Header Found')

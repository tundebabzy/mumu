from django.db import models
from django.contrib.auth.models import User
from django.utils import html

from accounts.models import Researcher, Editor

from db import mixin


class Code(models.Model):
    code = models.CharField(max_length=8)

    def __unicode__(self):
        return '%s' % self.code


class Question(models.Model, mixin.ModelDiffMixin):
    code = models.ForeignKey(Code)
    question_text = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    reference = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Researcher)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField()
    approved_by = models.ForeignKey(Editor, blank=True, null=True)

    def __unicode__(self):
        return '%s' % html.strip_tags(self.question_text)

    @models.permalink
    def get_absolute_url(self):
        return ('question', (), {'id': self.id})


class FlashCard(models.Model, mixin.ModelDiffMixin):
    code = models.ForeignKey(Code)
    question_text = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    reference = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Researcher)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField()
    approved_by = models.ForeignKey(Editor, blank=True, null=True)

    class Meta:
        verbose_name = 'Flash Card'

    def __unicode__(self):
        return self.question_text

    @models.permalink
    def get_absolute_url(self):
        return ('flashcard', (), {'pk': self.pk})


class Option(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    is_true = models.BooleanField()

    def __unicode__(self):
        return self.text


class Comment(models.Model, mixin.ModelDiffMixin):
    comment = models.TextField()
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return '%s' % self.comment


class Link(models.Model):
    description = models.CharField(max_length=100)
    link = models.URLField()
    question = models.ForeignKey(Question)


    def __unicode__(self):
        return '%s' % self.link


class AnswerLogs(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Option)
    time = models.DateTimeField(auto_now_add=True)


# SIGNAL TRIGGERED FUNCTIONS
#@receiver(post_save, sender=EditorComment)
#def correction_notification(sender, **kwargs):
#    editor_comment = kwargs['instance']
#    if editor_comment.has_changed:
#        question = editor_comment.question

#        subject = "mumu.com.ng: Your Editor Made A Comment About Your Question Entry"
#        from_email = settings.MAILER_USER
#        to_email = question.created_by.staff.user.email
#        message = """
#        Hi,\n Please have a look at the comment I made concerning your question entry: %s and perform the recommended action.\n My comment was : %s.\n Thanks.\n mumu.com.ng
#        """ % (question.id, editor_comment)
#        __password = settings.MAILER_USER_PASSWORD

#        try:
#            send_mail(subject, message, from_email, [to_email],
#                      fail_silently=False, auth_user=from_email,
#                      auth_password=__password)
#        except BadHeaderError:
#            return HttpResponse('Invalid header found')


#@receiver(post_save, sender=Question)
#def approval_notification(sender, **kwargs):
#    question = kwargs['instance']
#    if question.has_changed:
#        if 'approved' in question.changed_fields:
#            subject = 'mumu.com.ng: Approval notice'
#            from_email = settings.MAILER_USER
#            to_email = question.created_by.staff.user.email
#            message = """Hi,\n the approval status of your question entry #%s has changed. Please check the admin to check if your entry has been approved.\nThanks.\nmumu.com.ng""" % question.id
#            __password = settings.MAILER_USER_PASSWORD

#            try:
#                send_mail(subject, message, from_email, [to_email],
#                          fail_silently=False, auth_user=from_email,
#                          auth_password=__password)
#            except BadHeaderError:
#                return HttpResponse('Invalid Header Found')

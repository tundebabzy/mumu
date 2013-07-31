import hashlib
import random
import re

from registration.models import RegistrationProfile

from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class ContractType(models.Model):
    contract_type = models.CharField(max_length=10)

    def __unicode__(self):
        return self.contract_type

class Contract(models.Model):
    contract = models.ForeignKey(ContractType)
    start_date = models.DateField()

    def __unicode__(self):
        return self.contract.contract_type
        
class Department(models.Model):
    name = models.CharField(max_length=35)

    def __unicode__(self):
        return self.name

SHA1_RE = re.compile('^[a-f0-9]{40}$')

# The manager is a copy and paste from django-registration because when a base
# class which uses a custom manager is subclassed, the child class
# does not inherit the custom manager.

class RegistrationManager(models.Manager):
    """
    Custom manager for the ``RegistrationProfile`` model.
    
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.
    
    """
    def activate_user(self, activation_key):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.
        
        If the key is valid and has not expired, return the ``User``
        after activating.
        
        If the key is not valid or has expired, return ``False``.
        
        If the key is valid but the ``User`` is already active,
        return ``False``.
        
        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.

        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                profile.send_welcome_email()
                return user
        return False
    
    def create_inactive_user(self, username, email, password,
                             site, send_email=True):
        """
        Create a new, inactive ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, an activation email will be sent to the new
        user. To disable this, pass ``send_email=False``.
        
        """
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user)

        if send_email:
            registration_profile.send_activation_email(site)

        return new_user
    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def create_profile(self, user):
        """
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.
        
        The activation key for the ``RegistrationProfile`` will be a
        SHA1 hash, generated from a combination of the ``User``'s
        username and a random salt.
        
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt+username).hexdigest()
        return self.create(user=user,
                           activation_key=activation_key)
        
    def delete_expired_users(self):
        """
        Remove expired instances of ``RegistrationProfile`` and their
        associated ``User``s.
        
        Accounts to be deleted are identified by searching for
        instances of ``RegistrationProfile`` with expired activation
        keys, and then checking to see if their associated ``User``
        instances have the field ``is_active`` set to ``False``; any
        ``User`` who is both inactive and has an expired activation
        key will be deleted.
        
        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupregistration``.
        
        Regularly clearing out accounts which have never been
        activated serves two useful purposes:
        
        1. It alleviates the ocasional need to reset a
           ``RegistrationProfile`` and/or re-send an activation email
           when a user does not receive or does not act upon the
           initial activation email; since the account will be
           deleted, the user will be able to simply re-register and
           receive a new activation key.
        
        2. It prevents the possibility of a malicious user registering
           one or more accounts and never activating them (thus
           denying the use of those usernames to anyone else); since
           those accounts will be deleted, the usernames will become
           available for use again.
        
        If you have a troublesome ``User`` and wish to disable their
        account while keeping it in the database, simply delete the
        associated ``RegistrationProfile``; an inactive ``User`` which
        does not have an associated ``RegistrationProfile`` will not
        be deleted.
        
        """
        for profile in self.all():
            try:
                if profile.activation_key_expired():
                    user = profile.user
                    if not user.is_active:
                        user.delete()
                        profile.delete()
            except User.DoesNotExist:
                profile.delete()

class QuizzerProfile(RegistrationProfile):
    """
    A subclass of registration.models.RegistrationProfile which adds
    some extra fields and methods to the profile.
    """
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contract = models.ForeignKey(Contract, blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True)

    objects = RegistrationManager()

    # Child classes don't inherit Meta
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __unicode__(self):
        return u"Registration information for %s" % self.user

    def send_welcome_email(self):
        """
        Send a welcome email to the user associated with this
        ``RegistrationProfile``.
        """
        ctx_dict = {}
        subject = render_to_string('registration/welcome_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('registration/welcome_email.txt',
                                   ctx_dict)

        send_mail(subject, message, settings.WELCOME_EMAIL_USER,
            [self.user.email], fail_silently=False, 
            auth_user=settings.WELCOME_EMAIL_USER, 
            auth_password=settings.WELCOME_EMAIL_PASSWORD,
            connection=None)

class Manager(models.Model):
    staff = models.ForeignKey(QuizzerProfile)

    def __unicode__(self):
        return self.staff.user.get_full_name()

class Editor(models.Model):
    staff = models.ForeignKey(QuizzerProfile)

    def __unicode__(self):
        return self.staff.user.get_full_name()

class Researcher(models.Model):
    staff = models.ForeignKey(QuizzerProfile)

    def __unicode__(self):
        return self.staff.user.get_full_name()

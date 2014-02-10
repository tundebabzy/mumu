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

class Manager(models.Model):
    staff = models.ForeignKey(RegistrationProfile, null=True, blank=True)

    def __unicode__(self):
        return self.staff.user.__unicode__()
    
class Editor(models.Model):
    staff = models.ForeignKey(RegistrationProfile, null=True, blank=True)

    def __unicode__(self):
        return self.staff.user.__unicode__()

class Researcher(models.Model):
    staff = models.ForeignKey(RegistrationProfile, null=True, blank=True)

    def __unicode__(self):
        return self.staff.user.__unicode__()

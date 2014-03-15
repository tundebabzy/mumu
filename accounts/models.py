from registration.models import RegistrationProfile

from django.db import models

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

class NotifyMe(models.Model):
    email = models.EmailField(u'email address')
    level_name = models.CharField(max_length=15)

    def __unicode__(self):
        return '%s:%s' %(self.level_name, self.email)

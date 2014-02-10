# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContractType'
        db.create_table(u'accounts_contracttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contract_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'accounts', ['ContractType'])

        # Adding model 'Contract'
        db.create_table(u'accounts_contract', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.ContractType'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'accounts', ['Contract'])

        # Adding model 'Department'
        db.create_table(u'accounts_department', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal(u'accounts', ['Department'])

        # Adding model 'QuizzerProfile'
        db.create_table(u'accounts_quizzerprofile', (
            (u'registrationprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegistrationProfile'], unique=True, primary_key=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Contract'], null=True, blank=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Department'], null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['QuizzerProfile'])

        # Adding model 'Manager'
        db.create_table(u'accounts_manager', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.QuizzerProfile'])),
        ))
        db.send_create_signal(u'accounts', ['Manager'])

        # Adding model 'Editor'
        db.create_table(u'accounts_editor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.QuizzerProfile'])),
        ))
        db.send_create_signal(u'accounts', ['Editor'])

        # Adding model 'Researcher'
        db.create_table(u'accounts_researcher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.QuizzerProfile'])),
        ))
        db.send_create_signal(u'accounts', ['Researcher'])


    def backwards(self, orm):
        # Deleting model 'ContractType'
        db.delete_table(u'accounts_contracttype')

        # Deleting model 'Contract'
        db.delete_table(u'accounts_contract')

        # Deleting model 'Department'
        db.delete_table(u'accounts_department')

        # Deleting model 'QuizzerProfile'
        db.delete_table(u'accounts_quizzerprofile')

        # Deleting model 'Manager'
        db.delete_table(u'accounts_manager')

        # Deleting model 'Editor'
        db.delete_table(u'accounts_editor')

        # Deleting model 'Researcher'
        db.delete_table(u'accounts_researcher')


    models = {
        u'accounts.contract': {
            'Meta': {'object_name': 'Contract'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.ContractType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'accounts.contracttype': {
            'Meta': {'object_name': 'ContractType'},
            'contract_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'accounts.department': {
            'Meta': {'object_name': 'Department'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.QuizzerProfile']"})
        },
        u'accounts.manager': {
            'Meta': {'object_name': 'Manager'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.QuizzerProfile']"})
        },
        u'accounts.quizzerprofile': {
            'Meta': {'object_name': 'QuizzerProfile', '_ormbases': [u'registration.RegistrationProfile']},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Contract']", 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Department']", 'null': 'True', 'blank': 'True'}),
            u'registrationprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registration.RegistrationProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'accounts.researcher': {
            'Meta': {'object_name': 'Researcher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.QuizzerProfile']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'registration.registrationprofile': {
            'Meta': {'object_name': 'RegistrationProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['accounts']
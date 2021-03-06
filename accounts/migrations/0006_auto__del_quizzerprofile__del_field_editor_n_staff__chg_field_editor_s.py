# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'QuizzerProfile'
        db.delete_table(u'accounts_quizzerprofile')

        # Deleting field 'Editor.n_staff'
        db.delete_column(u'accounts_editor', 'n_staff_id')


        # Changing field 'Editor.staff'
        db.alter_column(u'accounts_editor', 'staff_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.RegistrationProfile']))
        # Deleting field 'Manager.n_staff'
        db.delete_column(u'accounts_manager', 'n_staff_id')


        # Changing field 'Manager.staff'
        db.alter_column(u'accounts_manager', 'staff_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.RegistrationProfile']))
        # Deleting field 'Researcher.n_staff'
        db.delete_column(u'accounts_researcher', 'n_staff_id')


        # Changing field 'Researcher.staff'
        db.alter_column(u'accounts_researcher', 'staff_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.RegistrationProfile']))

    def backwards(self, orm):
        # Adding model 'QuizzerProfile'
        db.create_table(u'accounts_quizzerprofile', (
            (u'registrationprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegistrationProfile'], unique=True, primary_key=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Contract'], null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Department'], null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['QuizzerProfile'])

        # Adding field 'Editor.n_staff'
        db.add_column(u'accounts_editor', 'n_staff',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='registration_profile_editor', null=True, to=orm['registration.RegistrationProfile'], blank=True),
                      keep_default=False)


        # Changing field 'Editor.staff'
        db.alter_column(u'accounts_editor', 'staff_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.RegistrationProfile'], null=True))
        # Adding field 'Manager.n_staff'
        db.add_column(u'accounts_manager', 'n_staff',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='registration_profile_manager', null=True, to=orm['registration.RegistrationProfile'], blank=True),
                      keep_default=False)


        # Changing field 'Manager.staff'
        db.alter_column(u'accounts_manager', 'staff_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.RegistrationProfile'], null=True))
        # Adding field 'Researcher.n_staff'
        db.add_column(u'accounts_researcher', 'n_staff',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='registration_profile_researcher', null=True, to=orm['registration.RegistrationProfile'], blank=True),
                      keep_default=False)


        # Changing field 'Researcher.staff'
        db.alter_column(u'accounts_researcher', 'staff_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.RegistrationProfile'], null=True))

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
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.RegistrationProfile']"})
        },
        u'accounts.manager': {
            'Meta': {'object_name': 'Manager'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.RegistrationProfile']"})
        },
        u'accounts.researcher': {
            'Meta': {'object_name': 'Researcher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.RegistrationProfile']"})
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
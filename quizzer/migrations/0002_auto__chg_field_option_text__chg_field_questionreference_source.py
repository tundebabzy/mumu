# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Option.text'
        db.alter_column('quizzer_option', 'text', self.gf('django.db.models.fields.TextField')())

        # Changing field 'QuestionReference.source'
        db.alter_column('quizzer_questionreference', 'source', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'Option.text'
        db.alter_column('quizzer_option', 'text', self.gf('django.db.models.fields.CharField')(max_length=90))

        # Changing field 'QuestionReference.source'
        db.alter_column('quizzer_questionreference', 'source', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        'accounts.contract': {
            'Meta': {'object_name': 'Contract'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.ContractType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'accounts.contracttype': {
            'Meta': {'object_name': 'ContractType'},
            'contract_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'accounts.department': {
            'Meta': {'object_name': 'Department'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.QuizzerProfile']"})
        },
        'accounts.quizzerprofile': {
            'Meta': {'object_name': 'QuizzerProfile', '_ormbases': ['registration.RegistrationProfile']},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Contract']", 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Department']", 'null': 'True', 'blank': 'True'}),
            'registrationprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegistrationProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        'accounts.researcher': {
            'Meta': {'object_name': 'Researcher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.QuizzerProfile']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'quizzer.answerlogs': {
            'Meta': {'object_name': 'AnswerLogs'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Option']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Question']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'quizzer.editorcomment': {
            'Meta': {'object_name': 'EditorComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Question']"})
        },
        'quizzer.exam': {
            'Meta': {'object_name': 'Exam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80'})
        },
        'quizzer.flashcard': {
            'Meta': {'object_name': 'FlashCard'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Editor']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Researcher']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Exam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Level']"}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Paper']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '300'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Topic']"})
        },
        'quizzer.level': {
            'Meta': {'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80'})
        },
        'quizzer.link': {
            'Meta': {'object_name': 'Link'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Question']"})
        },
        'quizzer.login': {
            'Meta': {'object_name': 'Login'},
            'http_user_agent': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'quizzer.option': {
            'Meta': {'object_name': 'Option'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_true': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'quizzer.optionexplanation': {
            'Meta': {'object_name': 'OptionExplanation'},
            'explanation': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Question']"})
        },
        'quizzer.paper': {
            'Meta': {'object_name': 'Paper'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80'})
        },
        'quizzer.payment': {
            'Meta': {'object_name': 'Payment'},
            'effective_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'has_used_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Level']", 'null': 'True', 'blank': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Paper']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'quizzer.question': {
            'Meta': {'object_name': 'Question'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Editor']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Researcher']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Exam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Level']"}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Paper']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Topic']"})
        },
        'quizzer.questionreference': {
            'Meta': {'object_name': 'QuestionReference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quizzer.Question']"}),
            'source': ('django.db.models.fields.TextField', [], {})
        },
        'quizzer.topic': {
            'Meta': {'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'})
        },
        'registration.registrationprofile': {
            'Meta': {'object_name': 'RegistrationProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['quizzer']
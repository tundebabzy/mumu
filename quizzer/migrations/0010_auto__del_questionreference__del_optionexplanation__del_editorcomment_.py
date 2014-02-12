# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'QuestionReference'
        db.delete_table(u'quizzer_questionreference')

        # Deleting model 'OptionExplanation'
        db.delete_table(u'quizzer_optionexplanation')

        # Deleting model 'EditorComment'
        db.delete_table(u'quizzer_editorcomment')

        # Adding model 'Comment'
        db.create_table(u'quizzer_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizzer.Question'])),
        ))
        db.send_create_signal(u'quizzer', ['Comment'])

        # Deleting field 'AnswerLogs.question'
        db.delete_column(u'quizzer_answerlogs', 'question_id')

        # Deleting field 'Question.text'
        db.delete_column(u'quizzer_question', 'text')


        # Changing field 'Question.code'
        db.alter_column(u'quizzer_question', 'code_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Code']))

        # Changing field 'Question.question_text'
        db.alter_column(u'quizzer_question', 'question_text', self.gf('django.db.models.fields.TextField')(default=''))
        # Deleting field 'FlashCard.text'
        db.delete_column(u'quizzer_flashcard', 'text')

        # Deleting field 'FlashCard.answer'
        db.delete_column(u'quizzer_flashcard', 'answer')


        # Changing field 'FlashCard.code'
        db.alter_column(u'quizzer_flashcard', 'code_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Code']))

        # Changing field 'FlashCard.question_text'
        db.alter_column(u'quizzer_flashcard', 'question_text', self.gf('django.db.models.fields.TextField')(default=''))

    def backwards(self, orm):
        # Adding model 'QuestionReference'
        db.create_table(u'quizzer_questionreference', (
            ('source', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizzer.Question'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'quizzer', ['QuestionReference'])

        # Adding model 'OptionExplanation'
        db.create_table(u'quizzer_optionexplanation', (
            ('explanation', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizzer.Question'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'quizzer', ['OptionExplanation'])

        # Adding model 'EditorComment'
        db.create_table(u'quizzer_editorcomment', (
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizzer.Question'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'quizzer', ['EditorComment'])

        # Deleting model 'Comment'
        db.delete_table(u'quizzer_comment')

        # Adding field 'AnswerLogs.question'
        db.add_column(u'quizzer_answerlogs', 'question',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Question']),
                      keep_default=False)

        # Adding field 'Question.text'
        db.add_column(u'quizzer_question', 'text',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


        # Changing field 'Question.code'
        db.alter_column(u'quizzer_question', 'code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizzer.Code'], null=True))

        # Changing field 'Question.question_text'
        db.alter_column(u'quizzer_question', 'question_text', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding field 'FlashCard.text'
        db.add_column(u'quizzer_flashcard', 'text',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'FlashCard.answer'
        db.add_column(u'quizzer_flashcard', 'answer',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


        # Changing field 'FlashCard.code'
        db.alter_column(u'quizzer_flashcard', 'code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizzer.Code'], null=True))

        # Changing field 'FlashCard.question_text'
        db.alter_column(u'quizzer_flashcard', 'question_text', self.gf('django.db.models.fields.TextField')(null=True))

    models = {
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.RegistrationProfile']", 'null': 'True', 'blank': 'True'})
        },
        u'accounts.researcher': {
            'Meta': {'object_name': 'Researcher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.RegistrationProfile']", 'null': 'True', 'blank': 'True'})
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
        u'quizzer.answerlogs': {
            'Meta': {'object_name': 'AnswerLogs'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Option']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'quizzer.code': {
            'Meta': {'object_name': 'Code'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'quizzer.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Question']"})
        },
        u'quizzer.flashcard': {
            'Meta': {'object_name': 'FlashCard'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Editor']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Code']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Researcher']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_text': ('django.db.models.fields.TextField', [], {}),
            'reference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'quizzer.link': {
            'Meta': {'object_name': 'Link'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Question']"})
        },
        u'quizzer.option': {
            'Meta': {'object_name': 'Option'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_true': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'quizzer.question': {
            'Meta': {'object_name': 'Question'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Editor']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Code']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Researcher']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_text': ('django.db.models.fields.TextField', [], {}),
            'reference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'registration.registrationprofile': {
            'Meta': {'object_name': 'RegistrationProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['quizzer']
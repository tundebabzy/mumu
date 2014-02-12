# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Login'
        db.delete_table(u'quizzer_login')

        # Deleting model 'Paper'
        db.delete_table(u'quizzer_paper')

        # Deleting model 'Payment'
        db.delete_table(u'quizzer_payment')

        # Deleting model 'Exam'
        db.delete_table(u'quizzer_exam')

        # Deleting model 'Level'
        db.delete_table(u'quizzer_level')

        # Deleting model 'Topic'
        db.delete_table(u'quizzer_topic')

        # Deleting field 'FlashCard.exam'
        db.delete_column(u'quizzer_flashcard', 'exam_id')

        # Deleting field 'FlashCard.topic'
        db.delete_column(u'quizzer_flashcard', 'topic_id')

        # Deleting field 'FlashCard.paper'
        db.delete_column(u'quizzer_flashcard', 'paper_id')

        # Deleting field 'FlashCard.slug'
        db.delete_column(u'quizzer_flashcard', 'slug')

        # Deleting field 'FlashCard.level'
        db.delete_column(u'quizzer_flashcard', 'level_id')

        # Adding field 'FlashCard.question_text'
        db.add_column(u'quizzer_flashcard', 'question_text',
                      self.gf('django.db.models.fields.TextField')(default='Flash Card', null=True),
                      keep_default=False)

        # Adding field 'FlashCard.explanation'
        db.add_column(u'quizzer_flashcard', 'explanation',
                      self.gf('django.db.models.fields.TextField')(default='explanation', null=True),
                      keep_default=False)

        # Adding field 'FlashCard.reference'
        db.add_column(u'quizzer_flashcard', 'reference',
                      self.gf('django.db.models.fields.TextField')(default='reference', null=True),
                      keep_default=False)

        # Deleting field 'Question.exam'
        db.delete_column(u'quizzer_question', 'exam_id')

        # Deleting field 'Question.topic'
        db.delete_column(u'quizzer_question', 'topic_id')

        # Deleting field 'Question.paper'
        db.delete_column(u'quizzer_question', 'paper_id')

        # Deleting field 'Question.level'
        db.delete_column(u'quizzer_question', 'level_id')

        # Adding field 'Question.question_text'
        db.add_column(u'quizzer_question', 'question_text',
                      self.gf('django.db.models.fields.TextField')(default='Question', null=True),
                      keep_default=False)

        # Adding field 'Question.explanation'
        db.add_column(u'quizzer_question', 'explanation',
                      self.gf('django.db.models.fields.TextField')(default='explanation', null=True),
                      keep_default=False)

        # Adding field 'Question.reference'
        db.add_column(u'quizzer_question', 'reference',
                      self.gf('django.db.models.fields.TextField')(default='reference', null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Login'
        db.create_table(u'quizzer_login', (
            ('http_user_agent', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'quizzer', ['Login'])

        # Adding model 'Paper'
        db.create_table(u'quizzer_paper', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=80)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'quizzer', ['Paper'])

        # Adding model 'Payment'
        db.create_table(u'quizzer_payment', (
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizzer.Paper'], null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizzer.Level'], null=True, blank=True)),
            ('effective_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('has_used_free', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'quizzer', ['Payment'])

        # Adding model 'Exam'
        db.create_table(u'quizzer_exam', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=80)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'quizzer', ['Exam'])

        # Adding model 'Level'
        db.create_table(u'quizzer_level', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=80)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'quizzer', ['Level'])

        # Adding model 'Topic'
        db.create_table(u'quizzer_topic', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'quizzer', ['Topic'])

        # Adding field 'FlashCard.exam'
        db.add_column(u'quizzer_flashcard', 'exam',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Exam']),
                      keep_default=False)

        # Adding field 'FlashCard.topic'
        db.add_column(u'quizzer_flashcard', 'topic',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Topic']),
                      keep_default=False)

        # Adding field 'FlashCard.paper'
        db.add_column(u'quizzer_flashcard', 'paper',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Paper']),
                      keep_default=False)

        # Adding field 'FlashCard.slug'
        db.add_column(u'quizzer_flashcard', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default=None, max_length=300),
                      keep_default=False)

        # Adding field 'FlashCard.level'
        db.add_column(u'quizzer_flashcard', 'level',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Level']),
                      keep_default=False)

        # Deleting field 'FlashCard.question_text'
        db.delete_column(u'quizzer_flashcard', 'question_text')

        # Deleting field 'FlashCard.explanation'
        db.delete_column(u'quizzer_flashcard', 'explanation')

        # Deleting field 'FlashCard.reference'
        db.delete_column(u'quizzer_flashcard', 'reference')

        # Adding field 'Question.exam'
        db.add_column(u'quizzer_question', 'exam',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Exam']),
                      keep_default=False)

        # Adding field 'Question.topic'
        db.add_column(u'quizzer_question', 'topic',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Topic']),
                      keep_default=False)

        # Adding field 'Question.paper'
        db.add_column(u'quizzer_question', 'paper',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Paper']),
                      keep_default=False)

        # Adding field 'Question.level'
        db.add_column(u'quizzer_question', 'level',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['quizzer.Level']),
                      keep_default=False)

        # Deleting field 'Question.question_text'
        db.delete_column(u'quizzer_question', 'question_text')

        # Deleting field 'Question.explanation'
        db.delete_column(u'quizzer_question', 'explanation')

        # Deleting field 'Question.reference'
        db.delete_column(u'quizzer_question', 'reference')


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
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Question']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'quizzer.code': {
            'Meta': {'object_name': 'Code'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'quizzer.editorcomment': {
            'Meta': {'object_name': 'EditorComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Question']"})
        },
        u'quizzer.flashcard': {
            'Meta': {'object_name': 'FlashCard'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Editor']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Code']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Researcher']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'default': "'explanation'", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_text': ('django.db.models.fields.TextField', [], {'default': "'Flash Card'", 'null': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'default': "'reference'", 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
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
        u'quizzer.optionexplanation': {
            'Meta': {'object_name': 'OptionExplanation'},
            'explanation': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Question']"})
        },
        u'quizzer.question': {
            'Meta': {'object_name': 'Question'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Editor']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Code']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Researcher']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'default': "'explanation'", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_text': ('django.db.models.fields.TextField', [], {'default': "'Question'", 'null': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'default': "'reference'", 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'quizzer.questionreference': {
            'Meta': {'object_name': 'QuestionReference'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizzer.Question']"}),
            'source': ('django.db.models.fields.TextField', [], {})
        },
        u'registration.registrationprofile': {
            'Meta': {'object_name': 'RegistrationProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['quizzer']
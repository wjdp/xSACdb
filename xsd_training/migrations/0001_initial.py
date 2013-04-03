# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PerformedLesson'
        db.create_table(u'xsd_training_performedlesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xsd_training.Session'])),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xsd_training.Lesson'])),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pl_instructor', to=orm['auth.User'])),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('private_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'xsd_training', ['PerformedLesson'])

        # Adding M2M table for field trainees on 'PerformedLesson'
        db.create_table(u'xsd_training_performedlesson_trainees', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('performedlesson', models.ForeignKey(orm[u'xsd_training.performedlesson'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'xsd_training_performedlesson_trainees', ['performedlesson_id', 'user_id'])

        # Adding model 'Lesson'
        db.create_table(u'xsd_training_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('qualification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xsd_training.Qualification'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('max_depth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('activities', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'xsd_training', ['Lesson'])

        # Adding model 'Qualification'
        db.create_table(u'xsd_training_qualification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
            ('definition', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('instructor_qualification', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'xsd_training', ['Qualification'])

        # Adding model 'SDC'
        db.create_table(u'xsd_training_sdc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('min_qualification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xsd_training.Qualification'])),
        ))
        db.send_create_signal(u'xsd_training', ['SDC'])

        # Adding model 'Session'
        db.create_table(u'xsd_training_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('where', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xsd_sites.Site'])),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'xsd_training', ['Session'])


    def backwards(self, orm):
        # Deleting model 'PerformedLesson'
        db.delete_table(u'xsd_training_performedlesson')

        # Removing M2M table for field trainees on 'PerformedLesson'
        db.delete_table('xsd_training_performedlesson_trainees')

        # Deleting model 'Lesson'
        db.delete_table(u'xsd_training_lesson')

        # Deleting model 'Qualification'
        db.delete_table(u'xsd_training_qualification')

        # Deleting model 'SDC'
        db.delete_table(u'xsd_training_sdc')

        # Deleting model 'Session'
        db.delete_table(u'xsd_training_session')


    models = {
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
        u'xsd_sites.site': {
            'Meta': {'object_name': 'Site'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facilities': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'max_depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_temp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_temp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'xsd_training.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'activities': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xsd_training.Qualification']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'xsd_training.performedlesson': {
            'Meta': {'object_name': 'PerformedLesson'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pl_instructor'", 'to': u"orm['auth.User']"}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xsd_training.Lesson']"}),
            'private_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xsd_training.Session']"}),
            'trainees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pl_trainees'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'xsd_training.qualification': {
            'Meta': {'object_name': 'Qualification'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor_qualification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'xsd_training.sdc': {
            'Meta': {'object_name': 'SDC'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xsd_training.Qualification']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'xsd_training.session': {
            'Meta': {'object_name': 'Session'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {}),
            'where': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xsd_sites.Site']"})
        }
    }

    complete_apps = ['xsd_training']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'MemberProfile.dob'
        db.delete_column(u'xsd_members_memberprofile', 'dob')


    def backwards(self, orm):
        # Adding field 'MemberProfile.dob'
        db.add_column(u'xsd_members_memberprofile', 'dob',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


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
        u'xsd_members.memberprofile': {
            'Meta': {'object_name': 'MemberProfile'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'alergies': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'associate_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'associate_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bsac_direct_debit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bsac_direct_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bsac_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bsac_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'bsac_member_via_another_club': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'club_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'club_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'club_membership_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xsd_members.MembershipType']", 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_open_graph': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'facebook_profile_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'instructor_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'medical_form_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'new_notify': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'next_of_kin_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'next_of_kin_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'next_of_kin_relation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'other_qualifications': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'qualifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['xsd_training.Qualification']", 'symmetrical': 'False', 'blank': 'True'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sdcs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['xsd_training.SDC']", 'symmetrical': 'False', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'training_for': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'q_training_for'", 'null': 'True', 'to': u"orm['xsd_training.Qualification']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'veggie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'xsd_members.membershiptype': {
            'Meta': {'object_name': 'MembershipType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'xsd_training.qualification': {
            'Meta': {'ordering': "['rank']", 'object_name': 'Qualification'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor_qualification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'xsd_training.sdc': {
            'Meta': {'ordering': "['title']", 'object_name': 'SDC'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interested_members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'min_qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xsd_training.Qualification']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['xsd_members']
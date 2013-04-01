# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Membership_Type'
        db.create_table(u'xsd_members_membership_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'xsd_members', ['Membership_Type'])

        # Adding field 'MemberProfile.dob'
        db.add_column(u'xsd_members_memberprofile', 'dob',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.address'
        db.add_column(u'xsd_members_memberprofile', 'address',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.postcode'
        db.add_column(u'xsd_members_memberprofile', 'postcode',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=11, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.home_phone'
        db.add_column(u'xsd_members_memberprofile', 'home_phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.mobile_phone'
        db.add_column(u'xsd_members_memberprofile', 'mobile_phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.next_of_kin_name'
        db.add_column(u'xsd_members_memberprofile', 'next_of_kin_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.next_of_kin_relation'
        db.add_column(u'xsd_members_memberprofile', 'next_of_kin_relation',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.next_of_kin_phone'
        db.add_column(u'xsd_members_memberprofile', 'next_of_kin_phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.veggie'
        db.add_column(u'xsd_members_memberprofile', 'veggie',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'MemberProfile.alergies'
        db.add_column(u'xsd_members_memberprofile', 'alergies',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.student_id'
        db.add_column(u'xsd_members_memberprofile', 'student_id',
                      self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.associate_id'
        db.add_column(u'xsd_members_memberprofile', 'associate_id',
                      self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.associate_expiry'
        db.add_column(u'xsd_members_memberprofile', 'associate_expiry',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.club_id'
        db.add_column(u'xsd_members_memberprofile', 'club_id',
                      self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.club_expiry'
        db.add_column(u'xsd_members_memberprofile', 'club_expiry',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.club_membership_type'
        db.add_column(u'xsd_members_memberprofile', 'club_membership_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xsd_members.Membership_Type'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.bsac_id'
        db.add_column(u'xsd_members_memberprofile', 'bsac_id',
                      self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.bsac_expiry'
        db.add_column(u'xsd_members_memberprofile', 'bsac_expiry',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.bsac_direct_member'
        db.add_column(u'xsd_members_memberprofile', 'bsac_direct_member',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'MemberProfile.bsac_member_via_another_club'
        db.add_column(u'xsd_members_memberprofile', 'bsac_member_via_another_club',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'MemberProfile.bsac_direct_debit'
        db.add_column(u'xsd_members_memberprofile', 'bsac_direct_debit',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'MemberProfile.medical_form_expiry'
        db.add_column(u'xsd_members_memberprofile', 'medical_form_expiry',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MemberProfile.other_qualifications'
        db.add_column(u'xsd_members_memberprofile', 'other_qualifications',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Membership_Type'
        db.delete_table(u'xsd_members_membership_type')

        # Deleting field 'MemberProfile.dob'
        db.delete_column(u'xsd_members_memberprofile', 'dob')

        # Deleting field 'MemberProfile.address'
        db.delete_column(u'xsd_members_memberprofile', 'address')

        # Deleting field 'MemberProfile.postcode'
        db.delete_column(u'xsd_members_memberprofile', 'postcode')

        # Deleting field 'MemberProfile.home_phone'
        db.delete_column(u'xsd_members_memberprofile', 'home_phone')

        # Deleting field 'MemberProfile.mobile_phone'
        db.delete_column(u'xsd_members_memberprofile', 'mobile_phone')

        # Deleting field 'MemberProfile.next_of_kin_name'
        db.delete_column(u'xsd_members_memberprofile', 'next_of_kin_name')

        # Deleting field 'MemberProfile.next_of_kin_relation'
        db.delete_column(u'xsd_members_memberprofile', 'next_of_kin_relation')

        # Deleting field 'MemberProfile.next_of_kin_phone'
        db.delete_column(u'xsd_members_memberprofile', 'next_of_kin_phone')

        # Deleting field 'MemberProfile.veggie'
        db.delete_column(u'xsd_members_memberprofile', 'veggie')

        # Deleting field 'MemberProfile.alergies'
        db.delete_column(u'xsd_members_memberprofile', 'alergies')

        # Deleting field 'MemberProfile.student_id'
        db.delete_column(u'xsd_members_memberprofile', 'student_id')

        # Deleting field 'MemberProfile.associate_id'
        db.delete_column(u'xsd_members_memberprofile', 'associate_id')

        # Deleting field 'MemberProfile.associate_expiry'
        db.delete_column(u'xsd_members_memberprofile', 'associate_expiry')

        # Deleting field 'MemberProfile.club_id'
        db.delete_column(u'xsd_members_memberprofile', 'club_id')

        # Deleting field 'MemberProfile.club_expiry'
        db.delete_column(u'xsd_members_memberprofile', 'club_expiry')

        # Deleting field 'MemberProfile.club_membership_type'
        db.delete_column(u'xsd_members_memberprofile', 'club_membership_type_id')

        # Deleting field 'MemberProfile.bsac_id'
        db.delete_column(u'xsd_members_memberprofile', 'bsac_id')

        # Deleting field 'MemberProfile.bsac_expiry'
        db.delete_column(u'xsd_members_memberprofile', 'bsac_expiry')

        # Deleting field 'MemberProfile.bsac_direct_member'
        db.delete_column(u'xsd_members_memberprofile', 'bsac_direct_member')

        # Deleting field 'MemberProfile.bsac_member_via_another_club'
        db.delete_column(u'xsd_members_memberprofile', 'bsac_member_via_another_club')

        # Deleting field 'MemberProfile.bsac_direct_debit'
        db.delete_column(u'xsd_members_memberprofile', 'bsac_direct_debit')

        # Deleting field 'MemberProfile.medical_form_expiry'
        db.delete_column(u'xsd_members_memberprofile', 'medical_form_expiry')

        # Deleting field 'MemberProfile.other_qualifications'
        db.delete_column(u'xsd_members_memberprofile', 'other_qualifications')


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
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'alergies': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'associate_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'associate_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'bsac_direct_debit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bsac_direct_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bsac_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bsac_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'bsac_member_via_another_club': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'club_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'club_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'club_membership_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xsd_members.Membership_Type']", 'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fid': ('django.db.models.fields.BigIntegerField', [], {}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medical_form_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'next_of_kin_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'next_of_kin_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'next_of_kin_relation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'other_qualifications': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'veggie': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'xsd_members.membership_type': {
            'Meta': {'object_name': 'Membership_Type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['xsd_members']
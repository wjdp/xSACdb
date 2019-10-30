# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xsd_training', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about_me', models.TextField(null=True, blank=True)),
                ('facebook_id', models.BigIntegerField(unique=True, null=True, blank=True)),
                ('access_token', models.TextField(help_text='Facebook token for offline access', null=True, blank=True)),
                ('facebook_name', models.CharField(max_length=255, null=True, blank=True)),
                ('facebook_profile_url', models.TextField(null=True, blank=True)),
                ('website_url', models.TextField(null=True, blank=True)),
                ('blog_url', models.TextField(null=True, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[('m', 'Male'), ('f', 'Female')])),
                ('raw_data', models.TextField(null=True, blank=True)),
                ('facebook_open_graph', models.NullBooleanField(help_text='Determines if this user want to share via open graph')),
                ('new_token_required', models.BooleanField(default=False, help_text='Set to true if the access token is outdated or lacks permissions')),
                ('image', models.ImageField(max_length=255, null=True, upload_to='images/facebook_profiles/%Y/%m/%d', blank=True)),
                ('token', models.CharField(max_length=150, blank=True)),
                ('new', models.BooleanField(default=True)),
                ('new_notify', models.BooleanField(default=True)),
                ('address', models.TextField(blank=True)),
                ('postcode', models.CharField(max_length=11, blank=True)),
                ('home_phone', models.CharField(max_length=20, blank=True)),
                ('mobile_phone', models.CharField(max_length=20, blank=True)),
                ('next_of_kin_name', models.CharField(max_length=40, blank=True)),
                ('next_of_kin_relation', models.CharField(max_length=20, blank=True)),
                ('next_of_kin_phone', models.CharField(max_length=20, blank=True)),
                ('veggie', models.BooleanField(default=False, verbose_name=b'Vegetarian')),
                ('alergies', models.TextField(verbose_name=b'Alergies and other requiements', blank=True)),
                ('instructor_number', models.IntegerField(null=True, blank=True)),
                ('student_id', models.IntegerField(max_length=7, null=True, blank=True)),
                ('associate_id', models.IntegerField(max_length=7, null=True, blank=True)),
                ('associate_expiry', models.DateField(null=True, blank=True)),
                ('club_id', models.IntegerField(max_length=7, null=True, blank=True)),
                ('club_expiry', models.DateField(null=True, blank=True)),
                ('bsac_id', models.IntegerField(max_length=7, null=True, verbose_name='BSAC ID', blank=True)),
                ('bsac_expiry', models.DateField(null=True, verbose_name='BSAC Expiry', blank=True)),
                ('bsac_direct_member', models.BooleanField(default=False, help_text=b'Adjusts the wording presented to the member when BSAC expires.', verbose_name='BSAC Direct Member')),
                ('bsac_member_via_another_club', models.BooleanField(default=False, help_text=b'Adjusts the wording presented to the member when BSAC expires.', verbose_name='BSAC member via another club')),
                ('bsac_direct_debit', models.BooleanField(default=False, verbose_name='BSAC Direct Debit')),
                ('medical_form_expiry', models.DateField(null=True, blank=True)),
                ('other_qualifications', models.TextField(blank=True)),
                ('is_instructor_cached', models.NullBooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MembershipType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='club_membership_type',
            field=models.ForeignKey(blank=True, to='xsd_members.MembershipType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='qualifications',
            field=models.ManyToManyField(to='xsd_training.Qualification', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='sdcs',
            field=models.ManyToManyField(to='xsd_training.SDC', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='top_instructor_qual_cached',
            field=models.ForeignKey(related_name='top_instructor_qual_cached', blank=True, to='xsd_training.Qualification', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='top_qual_cached',
            field=models.ForeignKey(related_name='top_qual_cached', blank=True, to='xsd_training.Qualification', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='training_for',
            field=models.ForeignKey(related_name='q_training_for', blank=True, to='xsd_training.Qualification', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

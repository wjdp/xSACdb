# -*- coding: utf-8 -*-


from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0015_remove_memberprofile_old_qualifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberprofile',
            name='archived',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='hidden',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='is_instructor_cached',
            field=models.NullBooleanField(default=None, editable=False),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='new_notify',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='token',
            field=models.CharField(max_length=150, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='top_instructor_qual_cached',
            field=models.ForeignKey(related_name='top_instructor_qual_cached', blank=True, editable=False, to='xsd_training.Qualification', null=True, on_delete=models.SET_NULL),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='top_qual_cached',
            field=models.ForeignKey(related_name='top_qual_cached', blank=True, editable=False, to='xsd_training.Qualification', null=True, on_delete=models.SET_NULL),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='user',
            field=models.OneToOneField(null=True, blank=True, editable=False, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
    ]

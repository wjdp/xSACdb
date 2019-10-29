# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0008_performed_qualification'),
        ('xsd_members', '0012_old_qualification_20170506_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberprofile',
            name='qualifications',
            field=models.ManyToManyField(related_name='members', through='xsd_training.PerformedQualification', to='xsd_training.Qualification', blank=True),
        ),
    ]

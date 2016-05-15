# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0007_auto_20160207_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberprofile',
            name='associate_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='bsac_id',
            field=models.IntegerField(null=True, verbose_name='BSAC ID', blank=True),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='club_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='student_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

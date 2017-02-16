# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0010_dynprofileform_20160530_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberprofile',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='veggie',
            field=models.NullBooleanField(default=None, help_text='Gives an indication to trip                                                                                 organisers for food requirements.', verbose_name='Vegetarian'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0006_remove_session_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualification',
            name='code',
            field=models.CharField(unique=True, max_length=4),
        ),
    ]

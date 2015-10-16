# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_kit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kit',
            name='club_owned',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kit',
            name='needs_testing',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loan',
            name='approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

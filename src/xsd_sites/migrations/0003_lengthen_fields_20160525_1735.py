# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_sites', '0002_auto_20160207_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(max_length=8, choices=[('TR', 'Training Site'), ('IN', 'Inland Site'), ('OF', 'Offshore Site')]),
        ),
    ]

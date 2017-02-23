# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_trips', '0004_reimplement_tweaks_20170218_0232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tripmember',
            name='accepted',
        ),
        migrations.AddField(
            model_name='tripmember',
            name='state',
            field=models.IntegerField(default=20, choices=[(20, 'Accepted')]),
        ),
    ]

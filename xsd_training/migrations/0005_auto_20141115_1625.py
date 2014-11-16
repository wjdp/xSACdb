# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0004_auto_20141115_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performedlesson',
            options={'ordering': ['trainee__last_name']},
        ),
    ]

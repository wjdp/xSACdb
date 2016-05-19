# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0003_auto_20141115_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memberprofile',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]

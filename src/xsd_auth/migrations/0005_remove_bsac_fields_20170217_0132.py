# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_auth', '0004_auto_20160515_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bsac_email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bsac_password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bsac_state',
        ),
    ]

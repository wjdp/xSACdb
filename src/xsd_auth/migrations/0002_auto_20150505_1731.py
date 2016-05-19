# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bsac_email',
            field=models.EmailField(default='', max_length=75, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='bsac_password',
            field=models.CharField(default='', max_length=128, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='bsac_state',
            field=models.CharField(default=b'N', max_length=1),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0005_auto_20141115_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='created_by',
        ),
    ]

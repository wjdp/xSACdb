# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performedlesson',
            options={'ordering': ['trainee__last_name']},
        ),
    ]

# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0003_user_fks_to_mp_fks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performedlesson',
            options={'ordering': ['trainee__user__last_name']},
        ),
        migrations.AlterField(
            model_name='session',
            name='when',
            field=models.DateTimeField(help_text=b'Formatted like: DD/MM/YYYY HH:MM'),
            preserve_default=True,
        ),
    ]

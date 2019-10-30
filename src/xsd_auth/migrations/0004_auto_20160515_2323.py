# -*- coding: utf-8 -*-


from django.db import migrations, models
import xsd_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_auth', '0003_auto_20160207_1755'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', xsd_auth.models.UserManager()),
            ],
        ),
    ]

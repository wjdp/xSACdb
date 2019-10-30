# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0006_update_mp_training_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberprofile',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]

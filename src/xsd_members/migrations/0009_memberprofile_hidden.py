# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0008_auto_20160515_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberprofile',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]

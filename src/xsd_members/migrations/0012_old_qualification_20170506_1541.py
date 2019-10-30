# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0011_archive_20170216_0055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberprofile',
            old_name='qualifications',
            new_name='old_qualifications',
        ),
    ]

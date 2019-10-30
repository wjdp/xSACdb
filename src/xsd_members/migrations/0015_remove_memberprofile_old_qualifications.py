# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0014_copy_existing_qualification_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberprofile',
            name='old_qualifications',
        ),
    ]

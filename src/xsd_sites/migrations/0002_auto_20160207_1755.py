# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_sites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]

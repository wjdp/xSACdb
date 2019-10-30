# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0008_performed_qualification'),
    ]

    operations = [
        migrations.AddField(
            model_name='performedqualification',
            name='mode',
            field=models.CharField(default='OTH', max_length=3, choices=[('INT', 'Internal'), ('EXT', 'External'), ('XO', 'Crossover'), ('OTH', 'Other')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='performedqualification',
            name='xo_from',
            field=models.CharField(max_length=64, null=True),
        ),
    ]

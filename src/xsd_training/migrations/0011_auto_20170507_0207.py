# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0010_auto_20170506_2228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performedqualification',
            options={'ordering': ['qualification__rank']},
        ),
        migrations.AlterField(
            model_name='performedqualification',
            name='mode',
            field=models.CharField(help_text='Internal: within this club, extenal: with another BSAC branch, crossover: from another agency.', max_length=3, choices=[('INT', 'Internal'), ('EXT', 'External'), ('XO', 'Crossover'), ('OTH', 'Other')]),
        ),
        migrations.AlterField(
            model_name='performedqualification',
            name='notes',
            field=models.TextField(help_text='Both instructors and the trainee can see any notes written here.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performedqualification',
            name='signed_off_by',
            field=models.ForeignKey(related_name='pqs_signed', on_delete=django.db.models.deletion.PROTECT, blank=True, to='xsd_members.MemberProfile', help_text='Who signed the QRB? Usually the branch DO.', null=True),
        ),
        migrations.AlterField(
            model_name='performedqualification',
            name='signed_off_on',
            field=models.DateField(help_text='Date when qualification was signed off in QRB.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performedqualification',
            name='xo_from',
            field=models.CharField(help_text='What qualification did the trainee crossover from?', max_length=64, null=True, verbose_name='Crossover From', blank=True),
        ),
    ]

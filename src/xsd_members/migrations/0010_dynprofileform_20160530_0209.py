# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0009_memberprofile_hidden'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberprofile',
            name='new',
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='alergies',
            field=models.TextField(help_text='This information is held for use by trip organisers. Please note anything                                            that would be important for both underwater activities and general trips,                                            details are held in confidence.', verbose_name='Alergies and other requiements', blank=True),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='bsac_member_via_another_club',
            field=models.BooleanField(default=False, help_text='Adjusts the wording presented to the member when                                                        BSAC membership expires.', verbose_name='BSAC member via another club'),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='next_of_kin_name',
            field=models.CharField(help_text='For an sport such as diving the practical activities involve some                                         level of risk, as such <strong>next of kin</strong> details are kept in case of                                         emergency. This data is only accessed when required. It will be taken in paper                                         form on trips.', max_length=40, blank=True),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='veggie',
            field=models.BooleanField(default=False, help_text='Gives an indication to trip                                                                             organisers for food requirements.', verbose_name='Vegetarian'),
        ),
    ]

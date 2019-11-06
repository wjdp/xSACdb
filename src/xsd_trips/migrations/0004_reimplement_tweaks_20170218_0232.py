# -*- coding: utf-8 -*-


from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_trips', '0003_reimplement_20170217_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='date_end',
            field=models.DateField(help_text='dd/mm/yyyy', null=True, verbose_name='Returns', blank=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='date_start',
            field=models.DateField(default=datetime.datetime(2017, 2, 18, 2, 32, 47, 721725), help_text='dd/mm/yyyy', verbose_name='Departs'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trip',
            name='max_depth',
            field=models.PositiveIntegerField(help_text='Indication of the maximum planned depth of dives.', null=True, verbose_name='Maximum depth', blank=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='min_qual',
            field=models.ForeignKey(blank=True, to='xsd_training.Qualification', help_text="Indication of the minimum qualification needed to participate on this trip's diving.", null=True, verbose_name='Minimum qualification', on_delete=models.SET_NULL),
        ),
        migrations.AlterField(
            model_name='trip',
            name='owner',
            field=models.ForeignKey(related_name='trip_owner', verbose_name='Organiser', to='xsd_members.MemberProfile', on_delete=models.SET_NULL),
        ),
        migrations.AlterField(
            model_name='trip',
            name='state',
            field=models.IntegerField(default=20, choices=[(10, 'Denied'), (20, 'New'), (40, 'Approved'), (45, 'Cancelled'), (50, 'Open'), (80, 'Closed'), (90, 'Completed')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'xsd_trips', '0001_initial'), (b'xsd_trips', '0002_remove_trip_trip_organiser'), (b'xsd_trips', '0003_reimplement_20170217_1601')]

    dependencies = [
        ('xsd_training', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xsd_sites', '0001_initial'),
        ('xsd_members', '0011_archive_20170216_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('cost', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('max_depth', models.PositiveIntegerField(null=True, blank=True)),
                ('spaces', models.PositiveIntegerField(null=True, blank=True)),
                ('min_qual', models.ForeignKey(to='xsd_training.Qualification')),
                ('date_end', models.DateField(null=True, blank=True)),
                ('date_start', models.DateField(null=True, blank=True)),
                ('description', models.TextField(help_text='Viewable by all members.', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TripMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('member', models.ForeignKey(to='xsd_members.MemberProfile')),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='owner',
            field=models.ForeignKey(related_name='trip_owner', default=0, to='xsd_members.MemberProfile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='state',
            field=models.IntegerField(default=20, choices=[(10, 'Cancelled'), (20, 'New'), (30, 'Pending'), (40, 'Approved'), (50, 'Accepting sign-ups'), (80, 'Closed'), (99, 'Completed')]),
        ),
        migrations.AlterField(
            model_name='trip',
            name='cost',
            field=models.DecimalField(help_text='Advertised cost of trip.', null=True, max_digits=6, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='max_depth',
            field=models.PositiveIntegerField(help_text='Indication of the maximum planned depth of dives.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='min_qual',
            field=models.ForeignKey(blank=True, to='xsd_training.Qualification', help_text="Indication of the minimum qualification needed to participate on this trip's diving.", null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='name',
            field=models.CharField(help_text='Friendly name.', max_length=64),
        ),
        migrations.AlterField(
            model_name='trip',
            name='spaces',
            field=models.PositiveIntegerField(help_text='Number of spaces to advertise.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tripmember',
            name='trip',
            field=models.ForeignKey(to='xsd_trips.Trip'),
        ),
        migrations.AddField(
            model_name='trip',
            name='members',
            field=models.ManyToManyField(related_name='trip_members', through='xsd_trips.TripMember', to=b'xsd_members.MemberProfile', blank=True),
        ),
    ]

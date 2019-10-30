# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xsd_training', '0001_initial'),
        ('xsd_sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('cost', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('max_depth', models.PositiveIntegerField(null=True, blank=True)),
                ('spaces', models.PositiveIntegerField(null=True, blank=True)),
                ('accepting_signups', models.BooleanField(default=True)),
                ('min_qual', models.ForeignKey(to='xsd_training.Qualification')),
                ('sites', models.ManyToManyField(to='xsd_sites.Site', blank=True)),
                ('trip_organiser', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TripAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('deposit_paid', models.BooleanField(default=False)),
                ('cost_paid', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('attendee', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('trip', models.ForeignKey(to='xsd_trips.Trip')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

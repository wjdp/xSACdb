# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0011_archive_20170216_0055'),
        ('xsd_trips', '0002_remove_trip_trip_organiser'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('member', models.ForeignKey(to='xsd_members.MemberProfile', on_delete=models.CASCADE)),
            ],
        ),
        migrations.RemoveField(
            model_name='tripattendee',
            name='attendee',
        ),
        migrations.RemoveField(
            model_name='tripattendee',
            name='trip',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='accepting_signups',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='date_from',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='date_to',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='location',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='sites',
        ),
        migrations.AddField(
            model_name='trip',
            name='date_end',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='date_start',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='description',
            field=models.TextField(help_text='Viewable by all members.', blank=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='owner',
            field=models.ForeignKey(related_name='trip_owner', default=0, to='xsd_members.MemberProfile', on_delete=models.SET_NULL),
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
            field=models.ForeignKey(blank=True, to='xsd_training.Qualification', help_text="Indication of the minimum qualification needed to participate on this trip's diving.", null=True, on_delete=models.SET_NULL),
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
        migrations.DeleteModel(
            name='TripAttendee',
        ),
        migrations.AddField(
            model_name='tripmember',
            name='trip',
            field=models.ForeignKey(to='xsd_trips.Trip', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='trip',
            name='members',
            field=models.ManyToManyField(related_name='trip_members', through='xsd_trips.TripMember', to='xsd_members.MemberProfile', blank=True),
        ),
    ]

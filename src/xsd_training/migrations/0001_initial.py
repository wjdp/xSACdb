# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xsd_sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=5, blank=True)),
                ('title', models.CharField(max_length=90)),
                ('mode', models.CharField(max_length=2, choices=[(b'TH', b'Theory'), (b'SW', b'Sheltered Water'), (b'OW', b'Open Water'), (b'DP', b'Dry Practical'), (b'XP', b'Experience'), (b'WS', b'Workshop'), (b'PQ', b'Post Qualification'), (b'XO', b'Cross-over'), (b'AS', b'Assessment')])),
                ('order', models.IntegerField(null=True, blank=True)),
                ('required', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('max_depth', models.IntegerField(null=True, blank=True)),
                ('activities', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['qualification', 'mode', 'order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PerformedLesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('partially_completed', models.BooleanField(default=False)),
                ('public_notes', models.TextField(blank=True)),
                ('private_notes', models.TextField(blank=True)),
                ('instructor', models.ForeignKey(related_name='pl_instructor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('lesson', models.ForeignKey(blank=True, to='xsd_training.Lesson', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PerformedSDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(null=True, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=3)),
                ('title', models.CharField(max_length=50)),
                ('rank', models.IntegerField()),
                ('definition', models.TextField(blank=True)),
                ('instructor_qualification', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['rank'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(max_length=3, choices=[(b'clu', b'Club Diving'), (b'saf', b'Safety and Rescue'), (b'sea', b'Seamanship'), (b'spe', b'Special Interest'), (b'tec', b'Technical')])),
                ('other_requirements', models.BooleanField(default=False)),
                ('interested_members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
                ('min_qualification', models.ForeignKey(blank=True, to='xsd_training.Qualification', null=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'SDC',
                'verbose_name_plural': 'SDCs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Optional name for session', max_length=64, blank=True)),
                ('when', models.DateTimeField(help_text=b'Formatted like: DD/MM/YYY HH:MM')),
                ('notes', models.TextField(help_text=b'Viewable by instructors and trainees in session.', blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('where', models.ForeignKey(to='xsd_sites.Site')),
            ],
            options={
                'ordering': ['when'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TraineeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('trainees', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='performedsdc',
            name='sdc',
            field=models.ForeignKey(to='xsd_training.SDC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='performedsdc',
            name='trainees',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='performedlesson',
            name='session',
            field=models.ForeignKey(blank=True, to='xsd_training.Session', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='performedlesson',
            name='trainee',
            field=models.ForeignKey(related_name='pl_trainee', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lesson',
            name='qualification',
            field=models.ForeignKey(to='xsd_training.Qualification'),
            preserve_default=True,
        ),
    ]

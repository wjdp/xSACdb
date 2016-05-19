# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('type', models.CharField(max_length=2, choices=[(b'TR', b'Training Site'), (b'IN', b'Inland Site'), (b'OF', b'Offshore Site')])),
                ('address', models.TextField(blank=True)),
                ('location', geoposition.fields.GeopositionField(max_length=42, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('min_temp', models.IntegerField(null=True, blank=True)),
                ('max_temp', models.IntegerField(null=True, blank=True)),
                ('max_depth', models.IntegerField(null=True, blank=True)),
                ('facilities', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

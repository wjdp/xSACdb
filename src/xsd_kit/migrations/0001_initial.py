# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('club_id', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=64, choices=[(b'WETS', b'Wetsuit'), (b'SEMI', b'Semidry'), (b'DRYS', b'Drysuit'), (b'BCD', b'BCD'), (b'WING', b'Wing'), (b'REGS', b'Regs'), (b'CYL', b'Cylinder'), (b'MASK', b'Mask'), (b'FINS', b'Fins'), (b'SNRK', b'Snorkel'), (b'COMP', b'Computer'), (b'TORH', b'Torch'), (b'SMB', b'SMB'), (b'DSMB', b'DSMB'), (b'REEL', b'Reel')])),
                ('size', models.CharField(max_length=64, blank=True)),
                ('club_owned', models.BooleanField()),
                ('cost', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('value', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('purchase_date', models.DateField(null=True, blank=True)),
                ('needs_testing', models.BooleanField()),
                ('test_date', models.DateField(null=True, blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
            ],
            options={
                'ordering': ['type', 'size', 'club_id'],
                'verbose_name': 'Kit',
                'verbose_name_plural': 'Bits of kit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.BooleanField()),
                ('notes', models.TextField(blank=True)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('kit', models.ManyToManyField(to='xsd_kit.Kit')),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

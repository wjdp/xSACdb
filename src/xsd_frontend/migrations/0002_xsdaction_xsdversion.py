# -*- coding: utf-8 -*-


from django.db import migrations, models
import reversion_compare.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('actstream', '0002_remove_action_data'),
        ('reversion', '0001_squashed_0004_auto_20160611_1202'),
        ('xsd_frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='XSDAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('actstream.action',),
        ),
        migrations.CreateModel(
            name='XSDVersion',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(reversion_compare.mixins.CompareMixin, 'reversion.version'),
        ),
    ]

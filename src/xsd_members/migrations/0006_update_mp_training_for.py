# -*- coding: utf-8 -*-


from django.db import migrations
from django.core.management import call_command

def update_mp_training_for(*args, **kwargs):
    call_command('update_mp_training_for')

class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0005_auto_djfb_to_allauth'),
    ]

    operations = [
        # Cannot run this here as it breaks on any field modifications to MemberProfile :'(
        #migrations.RunPython(update_mp_training_for),
    ]

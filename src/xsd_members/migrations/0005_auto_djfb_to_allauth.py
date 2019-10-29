# -*- coding: utf-8 -*-


from django.db import models, migrations

from allauth.socialaccount.models import SocialAccount

def copy_fb_data(apps, schema_editor):
    model = apps.get_model('xsd_members', 'MemberProfile')
    db_alias = schema_editor.connection.alias
    objects = model.objects.using(db_alias).all()
    for obj in objects:
        if obj.facebook_id:
            sa = SocialAccount(
                user_id = obj.user.pk,
                provider = 'facebook',
                uid = obj.facebook_id,
                last_login = obj.user.last_login,
                date_joined = obj.user.date_joined,
                extra_data = obj.raw_data
            )
            sa.save()


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0004_auto_20141115_1625'),
    ]

    operations = [
        migrations.RunPython(copy_fb_data),
        migrations.RemoveField(
            model_name='memberprofile',
            name='about_me',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='access_token',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='blog_url',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='facebook_id',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='facebook_name',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='facebook_open_graph',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='facebook_profile_url',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='new_token_required',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='raw_data',
        ),
        migrations.RemoveField(
            model_name='memberprofile',
            name='website_url',
        ),
    ]

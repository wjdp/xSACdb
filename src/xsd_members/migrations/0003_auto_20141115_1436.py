# -*- coding: utf-8 -*-


from django.db import models, migrations

def copypasta_user_fields(apps, schema_editor):
    model = apps.get_model('xsd_members', 'MemberProfile')
    db_alias = schema_editor.connection.alias
    objects = model.objects.using(db_alias).all()
    for obj in objects:
        obj.first_name = obj.user.first_name
        obj.last_name = obj.user.last_name
        obj.email = obj.user.email
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0002_auto_20141115_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberprofile',
            name='email',
            field=models.EmailField(default='premigrate@example.com', max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='first_name',
            field=models.CharField(default='Bobby', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='last_name',
            field=models.CharField(default='Premigrate', max_length=30),
            preserve_default=False,
        ),
        migrations.RunPython(copypasta_user_fields),
    ]

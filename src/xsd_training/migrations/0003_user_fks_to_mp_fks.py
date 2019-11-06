# -*- coding: utf-8 -*-


from django.db import models, migrations

user_data = {}

def migrate_user_to_mp(apps, schema_editor, changed_fields, model):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    # changed_fields=['request_made_by_id', 'response_by_id']
    model = apps.get_model('xsd_training', model)
    User = apps.get_model('xsd_auth', 'User')
    db_alias = schema_editor.connection.alias
    objects = model.objects.using(db_alias).all()
    for obj in objects:
        # print 'doing ' + str(obj.pk)
        for field in changed_fields:
            u_pk = getattr(obj, field)
            if u_pk:
                # print 'user '+str(u_pk)
                profile_pk = User.objects.get(pk=u_pk).memberprofile.id
                setattr(obj, field, profile_pk)
        obj.save()

def migrate_pl(apps, schema_editor):
    migrate_user_to_mp(apps, schema_editor,['instructor_id', 'trainee_id'],
        'PerformedLesson')

def store_m2m_user_data(apps, schema_editor, changed_fields, model_name):
    global user_data
    table = model_name.lower()
    model = apps.get_model('xsd_training', model_name)
    db_alias = schema_editor.connection.alias
    objects = model.objects.using(db_alias).all()
    for obj in objects:
        for field_name in changed_fields:
            field = getattr(obj, field_name)
            users = field.all()
            u_ids = []
            for user in users:
                u_ids.append(user.id)
            user_data['{}_{}_{}'.format(table,field_name,obj.id)] = u_ids


def migrate_m2m_user_to_mp(apps, schema_editor, changed_fields, model_name):
    global user_data
    table = model_name.lower()
    model = apps.get_model('xsd_training', model_name)
    User = apps.get_model('xsd_auth', 'User')
    db_alias = schema_editor.connection.alias
    objects = model.objects.using(db_alias).all()
    for obj in objects:
        for field_name in changed_fields:
            field = getattr(obj, field_name)
            muddled_users = user_data['{}_{}_{}'.format(table,field_name,obj.id)]
            profiles=[]
            if muddled_users != []:
                # print muddled_users
                for muser in muddled_users:
                    # We actually have
                    mp = User.objects.get(pk=muser).memberprofile
                    profiles.append(mp)
            field.clear()
            for profile in profiles:
                field.add(profile)
            obj.save()

def store_sdcs(apps, schema_editor):
    store_m2m_user_data(apps, schema_editor, ['interested_members'], 'SDC')
def store_traineegroups(apps, schema_editor):
    store_m2m_user_data(apps, schema_editor, ['trainees'], 'TraineeGroup')
def store_performedsdcs(apps, schema_editor):
    store_m2m_user_data(apps, schema_editor, ['trainees'], 'PerformedSDC')


def migrate_sdcs(apps, schema_editor):
    migrate_m2m_user_to_mp(apps, schema_editor, ['interested_members'], 'SDC')
def migrate_traineegroups(apps, schema_editor):
    migrate_m2m_user_to_mp(apps, schema_editor, ['trainees'], 'TraineeGroup')
def migrate_performedsdcs(apps, schema_editor):
    migrate_m2m_user_to_mp(apps, schema_editor, ['trainees'], 'PerformedSDC')


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0002_auto_20141109_1711'),
        ('xsd_members', '0001_initial'),
        ('xsd_auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_pl),
        migrations.RunPython(store_sdcs),
        migrations.RunPython(store_traineegroups),
        migrations.RunPython(store_performedsdcs),
        migrations.AlterField(
            model_name='performedlesson',
            name='instructor',
            field=models.ForeignKey(related_name='pl_instructor', blank=True, to='xsd_members.MemberProfile', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='performedlesson',
            name='trainee',
            field=models.ForeignKey(related_name='pl_trainee', to='xsd_members.MemberProfile', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='performedsdc',
            name='trainees',
            field=models.ManyToManyField(to='xsd_members.MemberProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sdc',
            name='interested_members',
            field=models.ManyToManyField(to='xsd_members.MemberProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='created_by',
            field=models.ForeignKey(blank=True, to='xsd_members.MemberProfile', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traineegroup',
            name='trainees',
            field=models.ManyToManyField(to='xsd_members.MemberProfile', blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(migrate_sdcs),
        migrations.RunPython(migrate_traineegroups),
        migrations.RunPython(migrate_performedsdcs),
    ]

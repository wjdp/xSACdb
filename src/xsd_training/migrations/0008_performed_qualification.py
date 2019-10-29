# -*- coding: utf-8 -*-


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_members', '0012_old_qualification_20170506_1541'),
        ('xsd_training', '0007_qual_codes_20160516_0044'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformedQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signed_off_on', models.DateField(null=True)),
                ('notes', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('qualification', models.ForeignKey(to='xsd_training.Qualification', on_delete=django.db.models.deletion.PROTECT)),
                ('signed_off_by', models.ForeignKey(related_name='pqs_signed', on_delete=django.db.models.deletion.PROTECT, to='xsd_members.MemberProfile', null=True)),
                ('trainee', models.ForeignKey(to='xsd_members.MemberProfile')),
            ],
        ),
        migrations.AlterModelOptions(
            name='performedlesson',
            options={'ordering': ['trainee__last_name'], 'get_latest_by': 'date'},
        ),
    ]

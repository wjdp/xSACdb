# -*- coding: utf-8 -*-



from django.db import migrations


def copy_qualifications(apps, schema_editor):
    MemberProfile = apps.get_model('xsd_members', 'MemberProfile')
    PerformedQualification = apps.get_model('xsd_training', 'PerformedQualification')
    
    for memberprofile in MemberProfile.objects.all():
        for qual in memberprofile.old_qualifications.all():
            pq = PerformedQualification(trainee=memberprofile, qualification=qual,
                                        notes='Qualification migrated from pre 0.4.x version of xSACdb')
            pq.save()


class Migration(migrations.Migration):
    dependencies = [
        ('xsd_members', '0013_memberprofile_qualifications'),
        ('xsd_training', '0008_performed_qualification'),
    ]

    operations = [
        migrations.RunPython(copy_qualifications),
    ]

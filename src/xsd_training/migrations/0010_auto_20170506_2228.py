# -*- coding: utf-8 -*-


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xsd_training', '0009_pq_modes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performedqualification',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performedqualification',
            name='signed_off_by',
            field=models.ForeignKey(related_name='pqs_signed', on_delete=django.db.models.deletion.PROTECT, blank=True, to='xsd_members.MemberProfile', null=True),
        ),
        migrations.AlterField(
            model_name='performedqualification',
            name='signed_off_on',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performedqualification',
            name='trainee',
            field=models.ForeignKey(editable=False, to='xsd_members.MemberProfile'),
        ),
        migrations.AlterField(
            model_name='performedqualification',
            name='xo_from',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]

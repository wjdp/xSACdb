# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xsd_training', '0001_initial'),
        ('xsd_sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.CharField(max_length=3, choices=[(b'mem', b'Membership Details and Renewal'), (b'tra', b'Training Records'), (b'sit', b'Dive Sites'), (b'tri', b'Trips')])),
                ('request_body', models.TextField()),
                ('response_body', models.TextField(blank=True)),
                ('completed', models.BooleanField(default=False, verbose_name=b'Mark this issue as fixed')),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(blank=True, to='xsd_training.Lesson', null=True, on_delete=models.CASCADE)),
                ('request_made_by', models.ForeignKey(related_name='request_made_by', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
                ('response_by', models.ForeignKey(related_name='response_by', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
                ('site', models.ForeignKey(blank=True, to='xsd_sites.Site', null=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

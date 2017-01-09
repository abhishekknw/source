# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0020_businessaccountcontact_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('assigned_by', models.ForeignKey(related_name='assigned_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('assigned_to', models.ForeignKey(related_name='assigned_to', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('campaign_id', models.ForeignKey(blank=True, to='v0.ProposalInfo', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='campaign_status',
            field=models.CharField(default='', max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='phase',
            field=models.CharField(default='', max_length=10, null=True, blank=True),
        ),
    ]

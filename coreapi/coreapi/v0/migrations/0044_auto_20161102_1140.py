# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0043_shortlistedinventorydetails_supplier_type_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignLeads',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign_id', models.IntegerField(default=0)),
                ('lead_email', models.EmailField(default='', max_length=254)),
                ('comments', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'campaign_leads',
            },
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('email', models.EmailField(max_length=254, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('gender', models.CharField(max_length=255, null=True, blank=True)),
                ('age', models.FloatField(null=True, blank=True)),
                ('phone', models.IntegerField(null=True, blank=True)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('status', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'lead',
            },
        ),
        migrations.AlterUniqueTogether(
            name='campaignleads',
            unique_together=set([('campaign_id', 'lead_email')]),
        ),
    ]

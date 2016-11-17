# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0033_spacebookingcost_supplier_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filter_name', models.CharField(max_length=255, null=True, blank=True)),
                ('filter_code', models.CharField(max_length=255, null=True, blank=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('center', models.ForeignKey(blank=True, to='v0.ProposalCenterMapping', null=True)),
            ],
            options={
                'db_table': 'filters',
            },
        ),
        migrations.AddField(
            model_name='proposalinfo',
            name='is_campaign',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='proposalinfo',
            name='parent',
            field=models.ForeignKey(default=None, blank=True, to='v0.ProposalInfo', null=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='center',
            field=models.ForeignKey(blank=True, to='v0.ProposalCenterMapping', null=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='proposal',
            field=models.ForeignKey(blank=True, to='v0.ProposalInfo', null=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='status',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalmastercost',
            name='proposal_version',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='filters',
            name='proposal',
            field=models.ForeignKey(blank=True, to='v0.ProposalInfo', null=True),
        ),
        migrations.AddField(
            model_name='filters',
            name='supplier_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
        ),
    ]

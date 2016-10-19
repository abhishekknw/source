# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0031_suppliertypebusshelter'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSciencesCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost', models.FloatField(null=True, blank=True)),
                ('comment', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'data_sciences_cost',
            },
        ),
        migrations.CreateModel(
            name='EventStaffingCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost', models.FloatField(null=True, blank=True)),
                ('comment', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'event_staffing_cost',
            },
        ),
        migrations.CreateModel(
            name='IdeationDesignCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost', models.FloatField(null=True, blank=True)),
                ('comment', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'ideation_design_cost',
            },
        ),
        migrations.CreateModel(
            name='LogisticOperationsCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost', models.FloatField(null=True, blank=True)),
                ('comment', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'logistic_operations_cost',
            },
        ),
        migrations.CreateModel(
            name='PrintingCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost', models.FloatField(null=True, blank=True)),
                ('comment', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'printing_cost',
            },
        ),
        migrations.CreateModel(
            name='ProposalMasterCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proposal_version', models.CharField(max_length=1000, null=True, blank=True)),
                ('agency_cost', models.FloatField(null=True, blank=True)),
                ('basic_cost', models.FloatField(null=True, blank=True)),
                ('discount', models.FloatField(null=True, blank=True)),
                ('total_cost', models.FloatField(null=True, blank=True)),
                ('tax', models.FloatField(null=True, blank=True)),
                ('total_impressions', models.FloatField(null=True, blank=True)),
                ('average_cost_per_impression', models.FloatField(null=True, blank=True)),
                ('proposal', models.OneToOneField(null=True, blank=True, to='v0.ProposalInfo')),
            ],
            options={
                'db_table': 'proposal_master_cost_details',
            },
        ),
        migrations.CreateModel(
            name='ProposalMetrics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metric_name', models.CharField(max_length=255, null=True, blank=True)),
                ('value', models.FloatField(null=True, blank=True)),
                ('proposal_master_cost', models.OneToOneField(null=True, blank=True, to='v0.ProposalMasterCost')),
                ('supplier_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'db_table': 'proposal_metrics',
            },
        ),
        migrations.CreateModel(
            name='SpaceBookingCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost', models.FloatField(null=True, blank=True)),
                ('comment', models.CharField(max_length=1000, null=True, blank=True)),
                ('proposal_master_cost', models.OneToOneField(null=True, blank=True, to='v0.ProposalMasterCost')),
            ],
            options={
                'db_table': 'space_booking_cost',
            },
        ),
        migrations.AddField(
            model_name='printingcost',
            name='proposal_master_cost',
            field=models.OneToOneField(null=True, blank=True, to='v0.ProposalMasterCost'),
        ),
        migrations.AddField(
            model_name='logisticoperationscost',
            name='proposal_master_cost',
            field=models.OneToOneField(null=True, blank=True, to='v0.ProposalMasterCost'),
        ),
        migrations.AddField(
            model_name='ideationdesigncost',
            name='proposal_master_cost',
            field=models.OneToOneField(null=True, blank=True, to='v0.ProposalMasterCost'),
        ),
        migrations.AddField(
            model_name='eventstaffingcost',
            name='proposal_master_cost',
            field=models.OneToOneField(null=True, blank=True, to='v0.ProposalMasterCost'),
        ),
        migrations.AddField(
            model_name='datasciencescost',
            name='proposal_master_cost',
            field=models.OneToOneField(null=True, blank=True, to='v0.ProposalMasterCost'),
        ),
    ]

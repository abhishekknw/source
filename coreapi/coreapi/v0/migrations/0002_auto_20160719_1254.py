# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryTypeVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_code', models.CharField(max_length=4, db_index=True)),
                ('poster_allowed', models.BooleanField(default=False)),
                ('poster_type', models.CharField(max_length=10, null=True, blank=True)),
                ('standee_allowed', models.BooleanField(default=False)),
                ('standee_type', models.CharField(max_length=10, null=True, blank=True)),
                ('flier_allowed', models.BooleanField(default=False)),
                ('flier_type', models.CharField(max_length=20, null=True, blank=True)),
                ('stall_allowed', models.BooleanField(default=False)),
                ('stall_type', models.CharField(max_length=10, null=True, blank=True)),
                ('banner_allowed', models.BooleanField(default=False)),
                ('banner_type', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'db_table': 'INVENTORY_TYPE_VERSION',
            },
        ),
        migrations.CreateModel(
            name='ProposalCenterMappingVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('center_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=150, null=True, blank=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('radius', models.FloatField()),
                ('subarea', models.CharField(max_length=35)),
                ('area', models.CharField(max_length=35)),
                ('city', models.CharField(max_length=35)),
                ('pincode', models.IntegerField()),
            ],
            options={
                'db_table': 'PROPOSAL_CENTER_MAPPING_VERSION',
            },
        ),
        migrations.CreateModel(
            name='ProposalInfoVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, db_column='NAME', blank=True)),
                ('payment_status', models.BooleanField(default=False, db_column='PAYMENT STATUS')),
                ('created_on', models.DateTimeField()),
                ('created_by', models.CharField(default='Admin', max_length=50)),
                ('tentative_cost', models.IntegerField(default=5000)),
                ('tentative_start_date', models.DateTimeField(null=True)),
                ('tentative_end_date', models.DateTimeField(null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('proposal', models.ForeignKey(related_name='proposal_versions', db_column='PROPOSAL', to='v0.ProposalInfo')),
            ],
            options={
                'db_table': 'PROPOSAL_INFO_VERSION',
            },
        ),
        migrations.CreateModel(
            name='ShortlistedSpacesVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_code', models.CharField(max_length=4)),
                ('object_id', models.CharField(max_length=12)),
                ('buffer_status', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(related_name='spaces_version', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'SHORTLISTED_SPACES_VERSION',
            },
        ),
        migrations.CreateModel(
            name='SpaceMappingVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('society_allowed', models.BooleanField(default=False)),
                ('society_count', models.IntegerField(default=0)),
                ('society_buffer_count', models.IntegerField(default=0)),
                ('corporate_allowed', models.BooleanField(default=False)),
                ('corporate_count', models.IntegerField(default=0)),
                ('corporate_buffer_count', models.IntegerField(default=0)),
                ('gym_allowed', models.BooleanField(default=False)),
                ('gym_count', models.IntegerField(default=0)),
                ('gym_buffer_count', models.IntegerField(default=0)),
                ('salon_allowed', models.BooleanField(default=False)),
                ('salon_count', models.IntegerField(default=0)),
                ('salon_buffer_count', models.IntegerField(default=0)),
                ('center_version', models.OneToOneField(related_name='space_mappings_version', to='v0.ProposalCenterMappingVersion')),
                ('proposal_version', models.ForeignKey(related_name='space_mapping_version', to='v0.ProposalInfoVersion')),
            ],
            options={
                'db_table': 'SPACE_MAPPING_VERSION',
            },
        ),
        migrations.RenameField(
            model_name='spacemapping',
            old_name='saloon_allowed',
            new_name='salon_allowed',
        ),
        migrations.RenameField(
            model_name='spacemapping',
            old_name='saloon_buffer_count',
            new_name='salon_buffer_count',
        ),
        migrations.RenameField(
            model_name='spacemapping',
            old_name='saloon_count',
            new_name='salon_count',
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='business_id',
            field=models.CharField(max_length=15, serialize=False, primary_key=True, db_column='BUSINESS_ID'),
        ),
        migrations.AddField(
            model_name='shortlistedspacesversion',
            name='space_mapping_version',
            field=models.ForeignKey(related_name='spaces_version', to='v0.SpaceMappingVersion'),
        ),
        migrations.AddField(
            model_name='proposalcentermappingversion',
            name='proposal_version',
            field=models.ForeignKey(related_name='centers_version', to='v0.ProposalInfoVersion'),
        ),
        migrations.AddField(
            model_name='inventorytypeversion',
            name='space_mapping_version',
            field=models.ForeignKey(related_name='inventory_types_version', to='v0.SpaceMappingVersion'),
        ),
        migrations.AlterUniqueTogether(
            name='proposalcentermappingversion',
            unique_together=set([('proposal_version', 'center_name')]),
        ),
    ]

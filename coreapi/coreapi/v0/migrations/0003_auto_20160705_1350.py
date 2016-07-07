# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_auto_20160705_1348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spacemapping',
            old_name='buffer_space_count',
            new_name='corporate_buffer_count',
        ),
        migrations.RenameField(
            model_name='spacemapping',
            old_name='space_count',
            new_name='corporate_count',
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='banner_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='banner_type',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='flier_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='flier_type',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='poster_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='poster_type',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='stall_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='stall_type',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='standee_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='standee_type',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='supplier_code',
            field=models.CharField(default='RS', max_length=4, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='supplier_code',
            field=models.CharField(default='RS', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='corporate_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='gym_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='gym_buffer_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='gym_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='saloon_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='saloon_buffer_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='saloon_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='society_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='society_buffer_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spacemapping',
            name='society_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='spacemapping',
            name='center',
            field=models.OneToOneField(related_name='space_mappings', to='v0.ProposalCenterMapping'),
        ),
        migrations.AlterUniqueTogether(
            name='inventorytype',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='spacemapping',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='inventory_name',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='inventory_type',
        ),
        migrations.RemoveField(
            model_name='spacemapping',
            name='inventory_type_count',
        ),
        migrations.RemoveField(
            model_name='spacemapping',
            name='space_name',
        ),
    ]

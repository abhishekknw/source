# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0066_data_migration_for_creating_organisation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactdetails',
            name='supplier',
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='comments',
            field=models.TextField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='department',
            field=models.CharField(max_length=155, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='designation',
            field=models.CharField(max_length=155, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='contact_authority',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='contact_type',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='country_code',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='email',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='landline',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='mobile',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='salutation',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='specify_others',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='spoc',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='std_code',
            field=models.CharField(max_length=6, null=True, blank=True),
        ),
    ]

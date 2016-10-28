# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0033_auto_20161020_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypebusshelter',
            name='supplier_code',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='account_number',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='averagerent',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='bank_name',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='building_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='constructedspace',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='constructionspaces_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='corporate_name',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='corporate_type',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='entryexit_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='floorperbuilding_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='ifsc_code',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='industry_segment',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='isrealestateallowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='luxurycars_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='openspace',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='openspaces_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='parkingspace',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='parkingspaces_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='possession_year',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='quantity_rating',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='standardcars_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='supplier_code',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='total_area',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='totalcompanies_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='totalemployees_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='totallift_count',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

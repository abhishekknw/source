# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0053_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypecorporate',
            name='corporate_name',
        ),
        migrations.RemoveField(
            model_name='suppliertypegym',
            name='gym_name',
        ),
        migrations.RemoveField(
            model_name='suppliertypegym',
            name='locality',
        ),
        migrations.RemoveField(
            model_name='suppliertypesalon',
            name='locality',
        ),
        migrations.RemoveField(
            model_name='suppliertypesalon',
            name='salon_name',
        ),
        migrations.AddField(
            model_name='flyerinventory',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='flyerinventory',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='area',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='bank_account_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='quality_rating',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='area',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='bank_account_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='quality_rating',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='area',
            field=models.CharField(default='', max_length=35),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='city',
            field=models.CharField(default='', max_length=35),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='pincode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='subarea',
            field=models.CharField(default='', max_length=35),
        ),
        migrations.AlterField(
            model_name='shortlistedspacesversion',
            name='space_mapping_version',
            field=models.ForeignKey(related_name='spaces_version', to='v0.SpaceMappingVersion'),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='account_number',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='averagerent',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='bank_name',
            field=models.CharField(max_length=250, null=True, blank=True),
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
            name='ifsc_code',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='latitude',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='locality_rating',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='longitude',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='luxurycars_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='machadalo_index',
            field=models.CharField(max_length=30, null=True, blank=True),
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
            name='quality_rating',
            field=models.CharField(max_length=50, null=True, blank=True),
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
            name='subarea',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='total_area',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='totallift_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='account_number',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='address1',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='address2',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='advertising_media',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='bank_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='banner_location',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='banner_places',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='banner_price_month',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='banner_price_week',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='category',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='chain_origin',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='city',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='dietchart_price',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='flyer_distribution',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='flyer_price_month',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='footfall_day',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='footfall_weekend',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='gym_type',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='gym_type_chain',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='ifsc_code',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='latitude',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='locality_rating',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='locker_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='locker_price_month',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='locker_price_week',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='longitude',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='machadalo_index',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='mirrorstrip_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='mirrorstrip_price_month',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='mirrorstrip_price_week',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='name',
            field=models.CharField(max_length=70, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='poster_places',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='poster_price_month',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='poster_price_week',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='stall_price_day',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='stall_price_two_day',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='standee_location',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='standee_places',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='standee_price_month',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='standee_price_two_week',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='standee_price_week',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='state',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='subarea',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='supplier_code',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='supplier_id',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='totalmembership_perannum',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='wall_price_month',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='wall_price_three_month',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='zipcode',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='account_number',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='address1',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='address2',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='bank_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='city',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='ifsc_code',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='latitude',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='locality_rating',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='longitude',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='machadalo_index',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='name',
            field=models.CharField(max_length=70, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='state',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='subarea',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='supplier_code',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='supplier_id',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='zipcode',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

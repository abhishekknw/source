# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0004_auto_20160113_1128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='past_year_collections_banners',
            new_name='past_collections_banners',
        ),
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='past_year_collections_car',
            new_name='past_collections_car',
        ),
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='past_year_collections_poster',
            new_name='past_collections_poster',
        ),
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='past_year_collections_stalls',
            new_name='past_collections_stalls',
        ),
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='past_year_collections_standee',
            new_name='past_collections_standee',
        ),
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='past_year_sponsorship_collection_events',
            new_name='past_sponsorship_collection_events',
        ),
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='past_year_total_sponsorship',
            new_name='past_total_sponsorship',
        ),
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='societies_preferred_business_id',
            new_name='preferred_business_id',
        ),
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='societies_preferred_business_type',
            new_name='preferred_business_type',
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='supplier',
            field=models.ForeignKey(related_name='stalls', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True),
        ),
    ]

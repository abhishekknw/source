# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0027_auto_20170109_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortlistedinventorypricingdetails',
            name='center',
        ),
        migrations.RemoveField(
            model_name='shortlistedinventorypricingdetails',
            name='proposal',
        ),
        migrations.RemoveField(
            model_name='shortlistedinventorypricingdetails',
            name='supplier_content_type',
        ),
        migrations.RemoveField(
            model_name='shortlistedinventorypricingdetails',
            name='supplier_id',
        ),
        migrations.RemoveField(
            model_name='shortlistedinventorypricingdetails',
            name='supplier_type_code',
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='inventory_content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0025_auto_20170109_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='supplier_content_type',
            field=models.ForeignKey(related_name='supplier_content_type', blank=True, to='contenttypes.ContentType', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AlterField(
            model_name='auditdate',
            name='audit_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 9, 14, 26, 45, 721945, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='closure_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 9, 14, 26, 45, 701720, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='inventory_content_type',
            field=models.ForeignKey(related_name='inventory_content_type', blank=True, to='contenttypes.ContentType', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 9, 14, 26, 45, 701685, tzinfo=utc)),
        ),
    ]

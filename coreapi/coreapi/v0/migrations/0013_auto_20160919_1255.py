# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from v0.models import SupplierTypeSociety


def populate(apps, schema_editor):
    """
    populates content_type, object_id, content_object of inventory_summary table
    assuming the existing rows  are only mapped to supplier_society table
    :param apps: apps
    :param schema_editor: editor
    :return: Nothing
    """
    myModel = apps.get_model('v0', 'InventorySummary')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    content_type = ContentType.objects.get(model='suppliertypesociety')

    for row in myModel.objects.all():
        supplier_type = SupplierTypeSociety.objects.get(supplier_id=row.supplier.supplier_id)
        row.content_type = content_type
        row.object_id = row.supplier.supplier_id
        row.content_object = supplier_type
        row.save()


class Migration(migrations.Migration):
    dependencies = [
        ('v0', '0012_auto_20160919_1254'),
    ]

    operations = [
        migrations.RunPython(populate),
    ]

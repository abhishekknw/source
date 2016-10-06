# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from v0.models import SupplierTypeSociety

def populate(apps, schema_editor):
    """
    populates content_type, object_id, content_object of inventory_summary table
    assuming the existing rows  are only mapped to supplier_society table
    :param apps: apps
    :param schema_editor: editor
    :return: Nothing
    """
    try:
        myModel = apps.get_model('v0', 'FlatType')
        ContentType = apps.get_model('contenttypes', 'ContentType')
        content_type = ContentType.objects.get(model='suppliertypesociety')

        for row in myModel.objects.all():
            supplier_type = SupplierTypeSociety.objects.get(supplier_id=row.society.supplier_id)
            row.content_type = content_type
            row.object_id = row.society.supplier_id
            row.content_object = supplier_type
            row.save()
    except Exception:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0017_auto_20160927_1315'),
    ]

    operations = [
    	migrations.RunPython(populate),
    ]

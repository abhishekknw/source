# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from v0.models import SupplierTypeSociety

from django.db import models, migrations


def populate_flat_type(apps, schema_editor):
    """
    :param apps:
    :param schema_editor:
    :return: counts rows in FlatType table associated with a supplier and store in SupplierSociety
    """
    supplier_model = apps.get_model('v0', 'SupplierTypeSociety')
    flat_type_model = apps.get_model('v0', 'FlatType')
    for row in supplier_model.objects.all():
        row.flat_type_count = flat_type_model.objects.filter(society=row).count()
        row.save()


class Migration(migrations.Migration):
    dependencies = [
        ('v0', '0013_auto_20160919_1255'),
    ]

    operations = [
        migrations.RunPython(populate_flat_type),
    ]

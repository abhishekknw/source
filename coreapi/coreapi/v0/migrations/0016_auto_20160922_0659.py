# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from v0.models import SupplierTypeSociety, ContactDetails, Events, FlyerInventory, ImageMapping, PosterInventory, \
    SocietyTower, StallInventory, StandeeInventory, WallInventory

"""
This migration populates object_id, content_type fields of these 9 models
"""


def do_each_model(myModel, content_type):
    """
    :param myModel: Model whose fields need to be populated
    :param content_type:  the content Type object
    :return: None
    """
    for row in myModel.objects.all():
        supplier_type = SupplierTypeSociety.objects.get(supplier_id=row.supplier.supplier_id)
        row.content_type = content_type
        row.object_id = row.supplier.supplier_id
        row.content_object = supplier_type
        row.save()


def populate_content_types(apps, schema):
    model_names = ['ContactDetails', 'Events', 'FlyerInventory', 'ImageMapping', 'PosterInventory', 'SocietyTower', \
                   'StallInventory', 'WallInventory'
                   ]
    load_names = [apps.get_model('v0', model) for model in model_names]
    ContentType = apps.get_model('contenttypes', 'ContentType')
    content_type = ContentType.objects.get(model='suppliertypesociety')
    for name in load_names:
        do_each_model(name, content_type)


class Migration(migrations.Migration):
    dependencies = [
        ('v0', '0015_auto_20160922_0658'),
    ]

    operations = [
        migrations.RunPython(populate_content_types),
    ]

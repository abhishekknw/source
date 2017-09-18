# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def fill_organisation(apps, schema_editor):
    """
    fills data from business_info table into organisation
    :param apps:
    :param schema_editor:
    :return:
    """
    business_info_model = apps.get_model(settings.APP_NAME, 'BusinessInfo')
    organisation_model = apps.get_model(settings.APP_NAME, 'Organisation')
    instances = business_info_model.objects.all()
    for instance in instances:

        data = {
            'name': instance.name,
            'user': instance.user,
            'organisation_id': instance.business_id,
            'type_name': instance.type_name,
            'sub_type': instance.sub_type,
            'phone': instance.phone,
            'email': instance.email,
            'address': instance.address,
            'reference_name': instance.reference_name,
            'reference_phone': instance.reference_phone,
            'reference_email': instance.reference_email,
            'comments': instance.comments,
            'category': 'BUSINESS',
        }
        organisation_model.objects.create(**data)


def empty_organisation(apps, schema_editor):
    """
    empties the organisation.
    """
    organisation_model = apps.get_model(settings.APP_NAME, 'Organisation')
    organisation_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0065_organisation'),
    ]

    operations = [
        migrations.RunPython(fill_organisation, reverse_code=empty_organisation)
    ]

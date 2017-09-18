# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def fill_contact_details(apps, schema_editor):
    """
    fills contacts from business account contact to contact details
    :param apps:
    :param schema_editor:
    :return:
    """
    business_account_contact_model = apps.get_model(settings.APP_NAME, 'BusinessAccountContact')
    contact_detail_model = apps.get_model(settings.APP_NAME, 'ContactDetails')

    for instance in business_account_contact_model.objects.all():
        data = {
            'content_type': instance.content_type,
            'object_id': instance.object_id,
            'name': instance.name,
            'designation': instance.designation,
            'department': instance.department,
            'mobile': int(instance.phone) if instance.phone else None,
            'email': instance.email,
            'spoc': instance.spoc,
            'comments': instance.comments
        }
        contact_detail_model.objects.create(**data)


def restore_contact_details(apps, schema_editor):
    """
    deletes any contact in contact details which came from business account contact
    :param apps:
    :param schema_editor:
    :return:
    """
    business_account_contact_model = apps.get_model(settings.APP_NAME, 'BusinessAccountContact')
    contact_detail_model = apps.get_model(settings.APP_NAME, 'ContactDetails')

    object_id_list = business_account_contact_model.objects.all().values_list('object_id', flat=True)
    contact_detail_model.objects.filter(object_id__in=object_id_list).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0067_auto_20170918_1253'),
    ]

    operations = [
        migrations.RunPython(fill_contact_details, reverse_code=restore_contact_details)
    ]

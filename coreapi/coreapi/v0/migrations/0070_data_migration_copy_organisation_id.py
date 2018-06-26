# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils import timezone

def fill_organisation_objects_from_business_objects_in_account_model(apps, schema_editor):
    """
    :param apps:
    :param schema_editor:
    :return:
    """
    account_info_model = apps.get_model(settings.APP_NAME, 'AccountInfo')
    organisation_model = apps.get_model(settings.APP_NAME, 'Organisation')

    for instance in account_info_model.objects.all():
        try:
            current_time = timezone.now()
            instance.organisation = organisation_model.objects.get(organisation_id=instance.business.business_id)
            if not instance.created_at:
                instance.created_at = current_time
            instance.updated_at = current_time
            instance.save()
        except Exception as e:
            pass

    generic_export_model = apps.get_model(settings.APP_NAME, 'GenericExportFileName')
    for instance in generic_export_model.objects.all():
        try:
            current_time = timezone.now()
            instance.organisation = organisation_model.objects.get(organisation_id=instance.business.business_id)
            if not instance.created_at:
                instance.created_at = current_time
            instance.updated_at = current_time
            instance.save()
        except Exception as e:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0069_auto_20170918_1320'),
    ]

    operations = [
        migrations.RunPython(fill_organisation_objects_from_business_objects_in_account_model)
    ]
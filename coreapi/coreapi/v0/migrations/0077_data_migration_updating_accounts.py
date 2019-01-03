# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models, migrations
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def update_account_organisation_field(apps, schema_editor):
    """
    :param apps:
    :param schema_editor:
    :return:
    """
    c = 0
    account_model = apps.get_model(settings.APP_NAME, 'AccountInfo')
    organisation_model = apps.get_model(settings.APP_NAME, 'Organisation')

    for instance in account_model.objects.all():
        if instance.business:
            try:
                instance.organisation = organisation_model.objects.get(pk=instance.business.pk)
                instance.save()
                c += 1
            except ObjectDoesNotExist:
                print('Organisation object does not exist for this business id {0}'.format(instance.business.pk))

    print('updated {0} accounts'.format(c))


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0076_create_machadalo_organisation'),
    ]

    operations = [
        migrations.RunPython(update_account_organisation_field)
    ]

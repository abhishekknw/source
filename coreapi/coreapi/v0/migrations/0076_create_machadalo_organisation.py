# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from v0.ui.website.utils import get_generic_id


def create_machadalo_organisation(apps, schema_editor):
    """
    :param apps:
    :param schema_editor:
    :return:
    """
    user = apps.get_model(settings.APP_NAME, 'BaseUser')
    admin, is_created = user.objects.get_or_create(username='admin', is_superuser=True)
    organisation_model = apps.get_model(settings.APP_NAME, 'Organisation')
    profile_model = apps.get_model(settings.APP_NAME, 'Profile')

    org = organisation_model.objects.create(
        name='MACHADALO',
        organisation_id=get_generic_id(['MACHADALO']),
        user=admin
    )
    profile = profile_model.objects.create(name='machadalo admin', organisation=org, is_standard=True)

    # admin.set_password('admin')
    admin.profile = profile
    admin.save()


class Migration(migrations.Migration):
    dependencies = [
        ('v0', '0075_organisationmap'),
    ]

    operations = [
        migrations.RunPython(create_machadalo_organisation)
    ]

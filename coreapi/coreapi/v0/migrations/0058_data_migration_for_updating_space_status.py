# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

import v0.constants as constants


def change_space_status(apps, schema_editor):
    """
    previously shortlisted spaces have status as 'X' which will be changed to 'S' and all spaces with status as
    'S' will be changed to 'F'.
    :param apps:
    :param schema_editor:
    :return:
    """
    shortlisted_space_model = apps.get_model(settings.APP_NAME, 'ShortlistedSpaces')
    # first mark all those shortlisted as finalized
    shortlisted_space_model.objects.filter(status=constants.shortlisted).update(status=constants.finalized)
    # then mark those which were not shortlisted as shortlisted
    shortlisted_space_model.objects.filter(status='X').update(status=constants.shortlisted)


def reverse_migration(apps, schema_editor):
    """
    reverses the above effect
    :param apps:
    :param schema_editor:
    :return:

    """
    shortlisted_space_model = apps.get_model(settings.APP_NAME, 'ShortlistedSpaces')
    # then mark those which were not shortlisted as shortlisted
    shortlisted_space_model.objects.filter(status=constants.shortlisted).update(status='X')
    # first mark all those shortlisted as finalized
    shortlisted_space_model.objects.filter(status=constants.finalized).update(status=constants.shortlisted)


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0057_auto_20170612_1034'),
    ]

    operations = [
        migrations.RunPython(change_space_status, reverse_code=reverse_migration)
    ]

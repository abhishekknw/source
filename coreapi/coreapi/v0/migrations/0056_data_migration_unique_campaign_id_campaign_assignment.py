# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def fix_campaign_assignment(apps, schema_editor):
    '''
    a campaign can be assigned to only one user as of now. There are multiple entries for a single campaign which
    we have to eleminate.
    :param apps:
    :param schema_editor:
    :return:
    '''
    campaign_assignment_model = apps.get_model(settings.APP_NAME, 'CampaignAssignment')
    instances = campaign_assignment_model.objects.all()
    campaign_instance_map = {}
    for instance in instances:
        campaign_id = instance.campaign.pk
        if not campaign_instance_map.get(campaign_id):
            campaign_instance_map[campaign_id] = []
        campaign_instance_map[campaign_id].append(instance)

    for campaign_id, instance_list in campaign_instance_map.iteritems():
        if len(instance_list) > 1:
            # delete everything except for the first object
            for instance in instance_list[1:]:
                instance.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0055_auto_20170605_1307'),
    ]

    operations = [
        migrations.RunPython(fix_campaign_assignment)
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0037_auto_20161020_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignbookinginfo',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='campaigninventoryprice',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='campaigninventoryprice',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='campaignothercost',
            name='campaign',
        ),
        migrations.DeleteModel(
            name='JMN_society',
        ),
        migrations.RemoveField(
            model_name='bannerinventory',
            name='photograph_1',
        ),
        migrations.RemoveField(
            model_name='bannerinventory',
            name='photograph_2',
        ),
        migrations.RemoveField(
            model_name='noticeboarddetails',
            name='photograph_1',
        ),
        migrations.RemoveField(
            model_name='noticeboarddetails',
            name='photograph_2',
        ),
        migrations.RemoveField(
            model_name='sportsinfra',
            name='photograph_1',
        ),
        migrations.RemoveField(
            model_name='sportsinfra',
            name='photograph_2',
        ),
        migrations.DeleteModel(
            name='CampaignBookingInfo',
        ),
        migrations.DeleteModel(
            name='CampaignInventoryPrice',
        ),
        migrations.DeleteModel(
            name='CampaignOtherCost',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0008_auto_20160420_0618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='flier_campaign',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='poster_campaign',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='stall_or_cd_campaign',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='standee_campaign',
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_campaign',
            field=models.IntegerField(null=True, db_column='FLIER_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='poster_campaign',
            field=models.IntegerField(null=True, db_column='POSTER_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='stall_or_cd_campaign',
            field=models.IntegerField(null=True, db_column='STALL_OR_CD_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='standee_campaign',
            field=models.IntegerField(null=True, db_column='STANDEE_CAMPAIGN', blank=True),
        ),
    ]

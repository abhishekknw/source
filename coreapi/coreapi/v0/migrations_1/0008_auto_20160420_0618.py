# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0007_auto_20160418_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='flier_campaign',
            field=models.IntegerField(null=True, db_column='FLIER_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='poster_campaign',
            field=models.IntegerField(null=True, db_column='POSTER_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='stall_or_cd_campaign',
            field=models.IntegerField(null=True, db_column='STALL_OR_CD_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='standee_campaign',
            field=models.IntegerField(null=True, db_column='STANDEE_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='total_campaign',
            field=models.IntegerField(null=True, db_column='TOTAL_CAMPAIGN', blank=True),
        ),
    ]

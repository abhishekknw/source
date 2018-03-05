# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0081_leadalias_leads'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorysummary',
            name='gateway_arch_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='gateway_arch_breadth',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='gateway_arch_length',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='lit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='non_lit',
            field=models.BooleanField(default=False),
        ),
    ]

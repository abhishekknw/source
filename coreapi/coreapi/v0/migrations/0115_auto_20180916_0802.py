# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-16 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0114_remove_leadsform_hot_lead_criteria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignassignment',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v0.ProposalInfo'),
        ),
    ]
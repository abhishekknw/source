# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-09 09:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0130_suppliertypesociety_supplier_phase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='supplier_phase',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-16 09:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0094_entry_id_added'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leadsformdata',
            old_name='leads_form_id',
            new_name='leads_form',
        ),
        migrations.RenameField(
            model_name='leadsformitems',
            old_name='leads_form_id',
            new_name='leads_form',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.apps import apps
from django.db import connection

# models on which we need to set DEFAULT value of user_id

names = [
 'auditor_society_mapping',
 'audits',
 'business_info',
 'campaign_leads',
 'django_admin_log',
 'signup',
 'supplier_bus_shelter',
 'supplier_corporate',
 'supplier_gym',
 'supplier_salon',
 'supplier_society',
 'user_areas',
 'user_cities',
 'user_profile' ,
 # 'auth_user_groups',
 # 'auth_user_user_permissions'
]


def set_default_user_id(apps, schema_editor):
    with connection.cursor() as cursor:
        for model in names:
            sql = 'ALTER TABLE `{0}` MODIFY COLUMN `user_id` integer DEFAULT 1 NOT NULL;'.format(model)
            cursor.execute(sql)


class Migration(migrations.Migration):
    dependencies = [
        ('v0', '0003_remove_businessaccountcontact_user'),
    ]

    operations = [
        migrations.RunPython(set_default_user_id)
    ]

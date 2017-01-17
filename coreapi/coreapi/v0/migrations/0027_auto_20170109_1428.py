# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0026_auto_20170109_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditdate',
            name='audit_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='closure_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='release_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

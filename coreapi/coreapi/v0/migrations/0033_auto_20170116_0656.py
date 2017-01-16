# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0032_auto_20170115_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditdate',
            name='audit_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='closure_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='release_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0031_auto_20170112_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditdate',
            name='audit_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='closure_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='release_date',
            field=models.DateTimeField(),
        ),
    ]

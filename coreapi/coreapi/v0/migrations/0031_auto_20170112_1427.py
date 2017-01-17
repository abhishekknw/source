# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0030_remove_shortlistedinventorypricingdetails_audit_dates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stallinventory',
            name='status',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='status',
        ),
    ]

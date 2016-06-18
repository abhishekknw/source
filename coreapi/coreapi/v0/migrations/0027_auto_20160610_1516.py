# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0026_corporateparkcompanylist_corporateparklargestemployers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corporateparklargestemployers',
            name='supplier_id',
        ),
        migrations.AddField(
            model_name='corporateparkcompanylist',
            name='largestemployers',
            field=models.BooleanField(default=False, db_column='LARGESTEMPLOYERS'),
        ),
        migrations.DeleteModel(
            name='CorporateParkLargestEmployers',
        ),
    ]

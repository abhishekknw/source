# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businesssubtypes',
            old_name='business',
            new_name='business_type',
        ),
        migrations.AlterField(
            model_name='business',
            name='sub_type',
            field=models.ForeignKey(related_name='sub_type_set', db_column='SUB_TYPE', to='v0.BusinessSubTypes'),
        ),
        migrations.AlterField(
            model_name='business',
            name='type',
            field=models.ForeignKey(related_name='type_set', db_column='TYPE', to='v0.BusinessTypes'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0030_contactdetailsgeneric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetailsgeneric',
            name='content_type',
            field=models.ForeignKey(related_name='contacts', to='contenttypes.ContentType'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0074_objectlevelpermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('first_organisation', models.ForeignKey(related_name='first_organisation', to='v0.Organisation', on_delete=django.db.models.deletion.CASCADE)),
                ('second_organisation', models.ForeignKey(related_name='second_organisation', to='v0.Organisation', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'organisation_map',
            },
        ),
    ]

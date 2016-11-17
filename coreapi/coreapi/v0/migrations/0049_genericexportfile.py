# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v0', '0048_auto_20161112_1014'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericExportFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2016, 11, 14, 7, 4, 24, 291333))),
                ('file_name', models.CharField(max_length=1000, null=True, blank=True)),
                ('account', models.ForeignKey(blank=True, to='v0.AccountInfo', null=True)),
                ('business', models.ForeignKey(blank=True, to='v0.BusinessInfo', null=True)),
                ('proposal', models.ForeignKey(blank=True, to='v0.ProposalInfo', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]

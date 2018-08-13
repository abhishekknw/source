# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0091_suppliertypesociety_representative'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTagImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('object_id', models.CharField(max_length=20)),
                ('image_path', models.CharField(max_length=1000, null=True, blank=True)),
                ('hashtag', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=1000, null=True, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('campaign', models.ForeignKey(to='v0.ProposalInfo')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'db_table': 'hashtag_images',
            },
        ),
    ]

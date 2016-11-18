# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0016_auto_20160914_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortlistedSpacesVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_code', models.CharField(max_length=4)),
                ('object_id', models.CharField(max_length=12)),
                ('buffer_status', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(related_name='spaces_version', to='contenttypes.ContentType')),
                ('space_mapping_version', models.ForeignKey(related_name='spaces_version', default=1, to='v0.SpaceMappingVersion')),
            ],
            options={
                'db_table': 'shortlisted_spaces_version',
            },
        ),
    ]

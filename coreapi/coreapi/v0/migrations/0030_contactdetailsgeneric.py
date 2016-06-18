# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0029_auto_20160611_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDetailsGeneric',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='CONTACT_ID')),
                ('contact_type', models.CharField(max_length=30, null=True, db_column='CONTACT_TYPE', blank=True)),
                ('name', models.CharField(max_length=50, null=True, db_column='CONTACT_NAME', blank=True)),
                ('salutation', models.CharField(max_length=50, null=True, db_column='SALUTATION', blank=True)),
                ('landline', models.BigIntegerField(null=True, db_column='CONTACT_LANDLINE', blank=True)),
                ('stdcode', models.CharField(max_length=6, null=True, db_column='STD_CODE', blank=True)),
                ('mobile', models.BigIntegerField(null=True, db_column='CONTACT_MOBILE', blank=True)),
                ('countrycode', models.CharField(max_length=10, null=True, db_column='COUNTRY_CODE', blank=True)),
                ('email', models.CharField(max_length=50, null=True, db_column='CONTACT_EMAILID', blank=True)),
                ('object_id', models.CharField(max_length=12)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'contact_details_generic',
            },
        ),
    ]

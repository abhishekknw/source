# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0039_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalCenterSuppliers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_type_code', models.CharField(max_length=255, null=True, blank=True)),
                ('center', models.ForeignKey(blank=True, to='v0.ProposalCenterMapping', null=True)),
                ('proposal', models.ForeignKey(blank=True, to='v0.ProposalInfo', null=True)),
                ('supplier_content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'db_table': 'proposal_center_suppliers',
            },
        ),
    ]

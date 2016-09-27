# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0014_auto_20160920_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactdetails',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='flyerinventory',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='flyerinventory',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='imagemapping',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='imagemapping',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='posterinventory',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='posterinventory',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='societytower',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='societytower',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='standeeinventory',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='standeeinventory',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='wallinventory',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='wallinventory',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
    ]

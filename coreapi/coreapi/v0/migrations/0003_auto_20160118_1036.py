# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_load_intial_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactdetails',
            old_name='contact_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='contactdetails',
            old_name='contact_landline',
            new_name='landline',
        ),
        migrations.RenameField(
            model_name='contactdetails',
            old_name='contact_mobile',
            new_name='mobile',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='contact_emailid',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='contact_name',
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='email',
            field=models.CharField(max_length=50, null=True, db_column='CONTACT_EMAILID', blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='name',
            field=models.CharField(max_length=50, null=True, db_column='CONTACT_NAME', blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='contact_type',
            field=models.CharField(max_length=30, null=True, db_column='CONTACT_TYPE', blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='specify_others',
            field=models.CharField(max_length=50, null=True, db_column='SPECIFY_OTHERS', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='business_id_not_allowed',
            field=models.CharField(max_length=50, null=True, db_column='BUSINESS_ID_NOT_ALLOWED', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='business_type_not_allowed',
            field=models.CharField(max_length=50, null=True, db_column='BUSINESS_TYPE_NOT_ALLOWED', blank=True),
        ),
    ]

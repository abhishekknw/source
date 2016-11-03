# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0031_suppliertypebusshelter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyfloor',
            name='company_details_id',
        ),
        migrations.RemoveField(
            model_name='corporatebuilding',
            name='corporatepark_id',
        ),
        migrations.RemoveField(
            model_name='corporatebuildingwing',
            name='building_id',
        ),
        migrations.RemoveField(
            model_name='corporatecompanydetails',
            name='company_id',
        ),
        migrations.RemoveField(
            model_name='corporateparkcompanylist',
            name='supplier_id',
        ),
        migrations.DeleteModel(
            name='CompanyFloor',
        ),
        migrations.DeleteModel(
            name='CorporateBuilding',
        ),
        migrations.DeleteModel(
            name='CorporateBuildingWing',
        ),
        migrations.DeleteModel(
            name='CorporateCompanyDetails',
        ),
        migrations.DeleteModel(
            name='CorporateParkCompanyList',
        ),
        migrations.DeleteModel(
            name='SupplierTypeCorporate',
        ),
    ]

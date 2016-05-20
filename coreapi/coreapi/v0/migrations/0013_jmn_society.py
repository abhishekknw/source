# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0012_auto_20160507_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='JMN_society',
            fields=[
                ('soc_id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('name', models.CharField(max_length=100, null=True, db_column='society_name', blank=True)),
                ('flats', models.CharField(max_length=15, null=True, db_column='flats', blank=True)),
                ('population', models.CharField(max_length=10, null=True, db_column='population', blank=True)),
                ('type', models.CharField(max_length=20, null=True, db_column='type', blank=True)),
                ('incomeGroup', models.CharField(max_length=15, null=True, db_column='incomeGroup', blank=True)),
                ('address', models.CharField(max_length=200, null=True, db_column='address', blank=True)),
                ('city', models.CharField(max_length=20, null=True, db_column='city', blank=True)),
                ('noticeBoard1', models.CharField(max_length=10, null=True, db_column='noticeBoard1', blank=True)),
                ('noticeBoard1LastDt', models.CharField(max_length=25, null=True, db_column='noticeBoard1LastDt', blank=True)),
                ('noticeBoard1Count', models.CharField(max_length=10, null=True, db_column='noticeBoard1Count', blank=True)),
                ('noticeBoard1Duration', models.CharField(max_length=10, null=True, db_column='noticeBoard1Duration', blank=True)),
                ('kiosk', models.CharField(max_length=10, null=True, db_column='kiosk', blank=True)),
                ('kioskLastDt', models.CharField(max_length=25, null=True, db_column='kioskLastDt', blank=True)),
                ('carDisplay', models.CharField(max_length=10, null=True, db_column='carDisplay', blank=True)),
                ('carDisplayLastDt', models.CharField(max_length=25, null=True, db_column='carDisplayLastDt', blank=True)),
                ('festivalStall', models.CharField(max_length=10, null=True, db_column='festivalStall', blank=True)),
                ('festivalStallLastDt', models.CharField(max_length=25, null=True, db_column='festivalStallLastDt', blank=True)),
                ('flyer', models.CharField(max_length=10, null=True, db_column='flyer', blank=True)),
                ('flyerDistributionMode', models.CharField(max_length=20, null=True, db_column='flyerDistributionMode', blank=True)),
                ('flyerLastDt', models.CharField(max_length=25, null=True, db_column='flyerLastDt', blank=True)),
                ('billJacketLastDt', models.CharField(max_length=25, null=True, db_column='billJacketLastDt', blank=True)),
                ('mainGate', models.CharField(max_length=10, null=True, db_column='mainGate', blank=True)),
                ('mainGateLastDt', models.CharField(max_length=20, null=True, db_column='mainGateLastDt', blank=True)),
                ('guardCharge', models.CharField(max_length=10, null=True, db_column='guardCharge', blank=True)),
                ('lat', models.CharField(max_length=15, null=True, db_column='latitude', blank=True)),
                ('lon', models.CharField(max_length=15, null=True, db_column='longitude', blank=True)),
                ('region', models.CharField(max_length=70, null=True, db_column='region', blank=True)),
                ('active', models.CharField(max_length=5, null=True, db_column='active', blank=True)),
                ('lastDt', models.CharField(max_length=25, null=True, db_column='lastDt', blank=True)),
                ('photo', models.CharField(max_length=100, null=True, db_column='photo', blank=True)),
                ('contact1Name', models.CharField(max_length=30, null=True, db_column='contact1Name', blank=True)),
                ('contact1Designation', models.CharField(max_length=15, null=True, db_column='contact1Designation', blank=True)),
                ('contact1Email', models.CharField(max_length=50, null=True, db_column='contact1Email', blank=True)),
                ('contact1Mobile', models.CharField(max_length=15, null=True, db_column='contact1Mobile', blank=True)),
                ('contact2Name', models.CharField(max_length=30, null=True, db_column='contact2Name', blank=True)),
                ('contact2Designation', models.CharField(max_length=15, null=True, db_column='contact2Designation', blank=True)),
                ('contact2Email', models.CharField(max_length=50, null=True, db_column='contact2Email', blank=True)),
                ('contact2Mobile', models.CharField(max_length=15, null=True, db_column='contact2Mobile', blank=True)),
                ('referredBy', models.CharField(max_length=20, null=True, db_column='referredBy', blank=True)),
                ('referredByEmail', models.CharField(max_length=40, null=True, db_column='referredByEmail', blank=True)),
                ('notPermitted', models.CharField(max_length=30, null=True, db_column='notPermitted', blank=True)),
                ('paymentMode', models.CharField(max_length=20, null=True, db_column='paymentMode', blank=True)),
                ('paymentDetail', models.CharField(max_length=20, null=True, db_column='paymentDetail', blank=True)),
            ],
            options={
                'db_table': 'jmn_society',
            },
        ),
    ]

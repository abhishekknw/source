# Generated by Django 2.1.4 on 2020-08-04 16:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0042_merge_20200801_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierBus',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('supplier_id', models.CharField(db_index=True, max_length=20, primary_key=True, serialize=False)),
                ('supplier_code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('locality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('quality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('machadalo_index', models.CharField(blank=True, max_length=30, null=True)),
                ('sales_allowed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'supplier_bus',
            },
        ),
        migrations.CreateModel(
            name='SupplierGantry',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('supplier_id', models.CharField(db_index=True, max_length=20, primary_key=True, serialize=False)),
                ('supplier_code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('locality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('quality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('machadalo_index', models.CharField(blank=True, max_length=30, null=True)),
                ('sales_allowed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'supplier_gantry',
            },
        ),
        migrations.CreateModel(
            name='SupplierRadioChannel',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('supplier_id', models.CharField(db_index=True, max_length=20, primary_key=True, serialize=False)),
                ('supplier_code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('locality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('quality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('machadalo_index', models.CharField(blank=True, max_length=30, null=True)),
                ('sales_allowed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'supplier_radio_channel',
            },
        ),
        migrations.CreateModel(
            name='SupplierTvChannel',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('supplier_id', models.CharField(db_index=True, max_length=20, primary_key=True, serialize=False)),
                ('supplier_code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('locality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('quality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('machadalo_index', models.CharField(blank=True, max_length=30, null=True)),
                ('sales_allowed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'supplier_tv_channel',
            },
        ),
    ]
# Generated by Django 2.1.4 on 2020-04-10 18:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0013_auto_20200410_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierHording',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('supplier_id', models.CharField(db_index=True, max_length=20, primary_key=True, serialize=False)),
                ('supplier_code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('locality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('quality_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('machadalo_index', models.CharField(blank=True, max_length=30, null=True)),
                ('address1', models.CharField(blank=True, max_length=252, null=True)),
                ('address2', models.CharField(blank=True, max_length=252, null=True)),
                ('area', models.CharField(blank=True, max_length=252, null=True)),
                ('subarea', models.CharField(blank=True, max_length=32, null=True)),
                ('city', models.CharField(blank=True, max_length=252, null=True)),
                ('state', models.CharField(blank=True, max_length=252, null=True)),
                ('zipcode', models.IntegerField(blank=True, max_length=252, null=True)),
                ('latitude', models.FloatField(blank=True, default=0.0, null=True)),
                ('longitude', models.FloatField(blank=True, default=0.0, max_length=252, null=True)),
                ('bank_account_name', models.CharField(blank=True, max_length=252, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=252, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=32, null=True)),
                ('account_number', models.CharField(blank=True, max_length=252, null=True)),
                ('food_tasting_allowed', models.BooleanField(default=False, null=True)),
                ('sales_allowed', models.BooleanField(default=False, null=True)),
                ('owner_name', models.CharField(blank=True, max_length=255, null=True)),
                ('external_Number', models.CharField(blank=True, max_length=255, null=True)),
                ('length', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('length_of_gantry', models.IntegerField(blank=True, null=True)),
                ('width_of_gantry', models.IntegerField(blank=True, null=True)),
                ('height_of_gantry', models.IntegerField(blank=True, null=True)),
                ('force_majeure_clause', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], max_length=10, null=True)),
                ('terms_around_print_mount', models.IntegerField(blank=True, null=True)),
                ('cost_per_sqft', models.IntegerField(blank=True, null=True)),
                ('cost_of_branding_space', models.IntegerField(blank=True, null=True)),
                ('printing_and_mounting_cost', models.IntegerField(blank=True, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=255, null=True)),
                ('cluster_of_hording', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], max_length=10, null=True)),
                ('traffic_junction', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('average_peakHourTraffic', models.CharField(blank=True, max_length=255, null=True)),
                ('average_nonPeakHourTraffic', models.CharField(blank=True, max_length=255, null=True)),
                ('average_pedestrianDailyCount', models.CharField(blank=True, max_length=255, null=True)),
                ('lit_status', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], max_length=10, null=True)),
                ('buses_count', models.IntegerField(blank=True, null=True)),
                ('sequence_number', models.IntegerField(blank=True, null=True)),
                ('signal_waiting_time', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'supplier_hording',
            },
        ),
    ]

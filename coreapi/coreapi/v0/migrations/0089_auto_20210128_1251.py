# Generated by Django 2.1.4 on 2021-01-28 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0088_auto_20210127_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_url', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=30, null=True)),
                ('gstin_number', models.CharField(blank=True, max_length=80, null=True)),
                ('registered_address', models.CharField(blank=True, max_length=500, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=50, null=True)),
                ('billing_address', models.CharField(blank=True, max_length=500, null=True)),
                ('pan_number', models.CharField(blank=True, max_length=50, null=True)),
                ('poc_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('designation', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='v0.Organisation')),
            ],
            options={
                'db_table': 'license_details',
            },
        ),
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_status', models.CharField(blank=True, max_length=30, null=True)),
                ('url', models.CharField(blank=True, max_length=80, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'payment_details',
            },
        ),
        migrations.AddField(
            model_name='requirement',
            name='client_status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Decision Pending', 'Decision Pending'), ('Decline', 'Decline')], default='Decision Pending', max_length=20),
        ),
    ]

# Generated by Django 2.1.4 on 2020-02-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0169_auto_20200218_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnershipDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('gst_number', models.CharField(blank=True, max_length=255, null=True)),
                ('pan_number', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, max_length=50, null=True)),
                ('end_date', models.DateField(blank=True, max_length=50, null=True)),
                ('payment_terms_condition', models.TextField(blank=True, max_length=255, null=True)),
                ('food_tasting', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], max_length=10, null=True)),
            ],
            options={
                'db_table': 'ownership_details',
            },
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='other_contact_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

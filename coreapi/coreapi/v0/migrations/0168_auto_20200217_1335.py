# Generated by Django 2.1.4 on 2020-02-17 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0167_auto_20200217_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplieramenitiesmap',
            name='amenity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplierAmenitiesMap', to='v0.Amenity'),
        ),
    ]
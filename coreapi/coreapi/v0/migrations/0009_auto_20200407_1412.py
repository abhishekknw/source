# Generated by Django 2.1.4 on 2020-04-07 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0008_auto_20200401_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressmaster',
            name='supplier_id',
            field=models.ForeignKey(max_length=20, on_delete=django.db.models.deletion.CASCADE, related_name='address_supplier', to='v0.SupplierMaster'),
        ),
    ]

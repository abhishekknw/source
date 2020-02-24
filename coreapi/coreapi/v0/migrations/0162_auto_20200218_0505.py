# Generated by Django 2.1.4 on 2020-02-18 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0161_auto_20200110_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='retail_shop_type',
            field=models.CharField(blank=True, choices=[('Toy Store', 'Toy Store'), ('Sports Goods', 'Sports Goods'), ('Electronic Goods', 'Electronic Goods'), ('Sanitary Goods', 'Sanitary Goods'), ('Grocery Goods', 'Grocery Goods'), ('Stationery Goods', 'Stationery Goods'), ('Merchandise Goods', 'Merchandise Goods'), ('Mobile Store', 'Mobile Store'), ('Mixed Store', 'Mixed Store'), ('Hypermart', 'Hypermart'), ('Jewelry Store', 'Jewelry Store'), ('Auto Dealership Store', 'Auto Dealership Store'), ('Shoes Store', 'Shoes Store'), ('Mall', 'Mall'), ('Gaming Zone', 'Gaming Zone'), ('FND (Food & Dining)', 'FND (Food & Dining)')], max_length=255, null=True),
        ),
    ]
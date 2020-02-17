# Generated by Django 2.1.4 on 2020-01-10 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0160_suppliertyperetailshop_landmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='retail_shop_type',
            field=models.CharField(blank=True, choices=[('GROCERY_STORE', 'GROCERY_STORE'), ('ELECTRONIC_STORE', 'ELECTRONIC_STORE'), ('SANITARY_STORE', 'SANITARY_STORE'), ('STATIONARY_STORE', 'STATIONARY_STORE'), ('Toy Store', 'Toy Store'), ('Toy Store', 'Toy Store'), ('Sports Goods', 'Sports Goods'), ('Electronic Goods', 'Electronic Goods'), ('Sanitary Goods', 'Sanitary Goods'), ('Grocery Goods', 'Grocery Goods'), ('Stationery Goods', 'Stationery Goods'), ('Merchandise Goods', 'Merchandise Goods'), ('Mobile Store', 'Mobile Store'), ('Mixed Store', 'Mixed Store'), ('Hypermart', 'Hypermart'), ('Jewelry Store', 'Jewelry Store'), ('Auto Dealership Store', 'Auto Dealership Store'), ('Shoes Store', 'Shoes Store'), ('Mall', 'Mall'), ('Gaming Zone', 'Gaming Zone'), ('FND (Food & Dining)', 'FND (Food & Dining)')], max_length=255, null=True),
        ),
    ]
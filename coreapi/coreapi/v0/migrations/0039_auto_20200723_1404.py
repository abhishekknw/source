# Generated by Django 2.1.4 on 2020-07-23 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0038_auto_20200708_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypecode',
            name='supplier_type_name',
            field=models.CharField(db_column='SUPPLIER_TYPE_NAME', max_length=35, null=True),
        ),
    ]
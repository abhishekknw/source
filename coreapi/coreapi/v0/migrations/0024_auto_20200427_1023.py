# Generated by Django 2.1.4 on 2020-04-27 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0023_auto_20200422_0954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addressmaster',
            old_name='supplier_id',
            new_name='supplier',
        ),
    ]

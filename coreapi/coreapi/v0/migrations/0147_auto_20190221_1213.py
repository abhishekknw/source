# Generated by Django 2.1.4 on 2019-02-21 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0146_supplierassignment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplierassignment',
            old_name='object_id',
            new_name='supplier_id',
        ),
    ]

# Generated by Django 2.1.4 on 2020-09-22 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0060_auto_20200922_0635'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='varified_bd_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='requirement',
            name='varified_ops_date',
            field=models.DateTimeField(null=True),
        ),
    ]

# Generated by Django 2.1.4 on 2020-03-06 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_auto_20200306_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplieramenitiesmap',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
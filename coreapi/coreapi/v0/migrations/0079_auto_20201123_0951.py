# Generated by Django 2.1.4 on 2020-11-23 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0078_auto_20201123_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='comment',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]

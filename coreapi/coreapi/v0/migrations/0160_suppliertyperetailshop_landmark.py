# Generated by Django 2.1.4 on 2020-01-07 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0159_auto_20200106_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertyperetailshop',
            name='landmark',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]

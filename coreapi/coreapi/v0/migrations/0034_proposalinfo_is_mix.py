# Generated by Django 2.1.4 on 2020-06-04 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0033_auto_20200525_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalinfo',
            name='is_mix',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 2.1.4 on 2021-01-25 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0087_auto_20210125_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='designation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

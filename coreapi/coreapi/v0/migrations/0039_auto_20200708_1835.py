# Generated by Django 2.1.4 on 2020-07-08 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0038_auto_20200708_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeofendcustomer',
            name='formatted_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shortlistedspaces',
            name='booking_status',
            field=models.CharField(default='NI', max_length=10),
        ),
    ]

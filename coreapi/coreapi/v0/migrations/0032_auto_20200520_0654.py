# Generated by Django 2.1.4 on 2020-05-20 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0031_posterliftinventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedspaces',
            name='account_number',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='beneficiary_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='payment_message',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

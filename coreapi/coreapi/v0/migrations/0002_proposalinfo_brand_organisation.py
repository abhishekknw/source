# Generated by Django 2.1.4 on 2020-03-03 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalinfo',
            name='brand_organisation',
            field=models.IntegerField(default=11),
        ),
    ]
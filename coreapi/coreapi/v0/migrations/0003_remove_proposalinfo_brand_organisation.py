# Generated by Django 2.1.4 on 2020-03-03 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_proposalinfo_brand_organisation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalinfo',
            name='brand_organisation',
        ),
    ]

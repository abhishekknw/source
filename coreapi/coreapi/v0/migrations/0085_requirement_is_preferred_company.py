# Generated by Django 2.1.4 on 2021-01-08 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0084_auto_20201216_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='is_preferred_company',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=5),
        ),
    ]

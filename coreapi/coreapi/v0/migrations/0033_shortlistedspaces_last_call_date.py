# Generated by Django 2.1.4 on 2020-11-19 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0032_auto_20200520_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedspaces',
            name='last_call_date',
            field=models.DateTimeField(null=True),
        ),
    ]

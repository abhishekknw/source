# Generated by Django 2.1.4 on 2019-12-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0156_shortlistedspaces_next_action_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='emailVerifyCode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
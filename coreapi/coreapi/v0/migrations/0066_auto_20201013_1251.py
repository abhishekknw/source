# Generated by Django 2.1.4 on 2020-10-13 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0065_auto_20201007_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='current_patner_feedback_reason',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]
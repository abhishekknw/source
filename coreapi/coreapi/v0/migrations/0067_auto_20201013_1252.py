# Generated by Django 2.1.4 on 2020-10-13 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0066_auto_20201013_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='current_patner_feedback_reason',
            field=models.CharField(blank=True, max_length=250, null=''),
        ),
    ]

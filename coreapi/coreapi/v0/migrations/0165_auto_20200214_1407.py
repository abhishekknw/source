# Generated by Django 2.1.4 on 2020-02-14 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0164_suppliertypesociety_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='budget',
            field=models.IntegerField(blank=True, db_column='EVENT_BUDGET', null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='last_year_sponsors',
            field=models.CharField(blank=True, db_column='EVENT_LAST_YEAR_SPONSORS', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='supplieramenitiesmap',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
# Generated by Django 2.1.4 on 2020-10-03 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0061_auto_20200922_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierbus',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='suppliereducationalinstitute',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='suppliereducationalinstitute',
            name='educationBoard',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='suppliereducationalinstitute',
            name='inst_sub_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='suppliereducationalinstitute',
            name='inst_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='suppliergantry',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='supplierradiochannel',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='suppliertvchannel',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='footfall_week',
            field=models.IntegerField(blank=True, db_column='FOOTFALL_WEEL', null=True),
        ),
    ]

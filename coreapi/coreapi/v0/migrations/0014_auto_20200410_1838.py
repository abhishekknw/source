# Generated by Django 2.1.4 on 2020-04-10 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0013_auto_20200410_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypebusshelter',
            name='average_footfall_daily_count',
        ),
        migrations.RemoveField(
            model_name='suppliertypecorporate',
            name='landmark',
        ),
        migrations.RemoveField(
            model_name='suppliertypecorporate',
            name='totalemployees_count',
        ),
        migrations.RemoveField(
            model_name='suppliertypegym',
            name='footfall_weekend',
        ),
        migrations.RemoveField(
            model_name='suppliertyperetailshop',
            name='average_weekday',
        ),
        migrations.RemoveField(
            model_name='suppliertyperetailshop',
            name='average_weekend',
        ),
        migrations.RemoveField(
            model_name='suppliertypesalon',
            name='footfall_week',
        ),
        migrations.RemoveField(
            model_name='suppliertypesalon',
            name='footfall_weekend',
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='account_number',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='address1',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='address2',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='area',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='bank_account_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='bank_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='city',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='longitude',
            field=models.FloatField(blank=True, default=0.0, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='sales_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='state',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='subarea',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='zipcode',
            field=models.IntegerField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='account_number',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='address1',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='address2',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='area',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='bank_account_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='bank_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='city',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='longitude',
            field=models.FloatField(blank=True, default=0.0, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='sales_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='state',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='subarea',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='zipcode',
            field=models.IntegerField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='account_number',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='address1',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='address2',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='area',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='bank_account_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='bank_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='city',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='longitude',
            field=models.FloatField(blank=True, default=0.0, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='sales_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='state',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='subarea',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='zipcode',
            field=models.IntegerField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='account_number',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='address1',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='address2',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='area',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='bank_account_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='bank_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='city',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='longitude',
            field=models.FloatField(blank=True, default=0.0, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='sales_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='state',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='subarea',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='zipcode',
            field=models.IntegerField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='account_number',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='address1',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='address2',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='area',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='bank_account_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='bank_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='city',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='longitude',
            field=models.FloatField(blank=True, default=0.0, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='sales_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='state',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='subarea',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='zipcode',
            field=models.IntegerField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='account_number',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='address1',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='address2',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='area',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='bank_account_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='bank_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='city',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='longitude',
            field=models.FloatField(blank=True, default=0.0, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='sales_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='state',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='subarea',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='zipcode',
            field=models.IntegerField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='account_number',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='address1',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='address2',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='area',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='bank_account_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='bank_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='city',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='longitude',
            field=models.FloatField(blank=True, default=0.0, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='sales_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='state',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='subarea',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='zipcode',
            field=models.IntegerField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='account_number',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='address1',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='address2',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='area',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='bank_account_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='bank_name',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='city',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='longitude',
            field=models.FloatField(blank=True, default=0.0, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='sales_allowed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='state',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='subarea',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='zipcode',
            field=models.IntegerField(blank=True, max_length=252, null=True),
        ),
    ]

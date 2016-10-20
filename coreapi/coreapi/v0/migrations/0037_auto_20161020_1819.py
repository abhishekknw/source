# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0036_suppliertypegym_suppliertypesalon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypecorporate',
            name='corporate_name',
        ),
        migrations.RemoveField(
            model_name='suppliertypegym',
            name='gym_name',
        ),
        migrations.RemoveField(
            model_name='suppliertypesalon',
            name='salon_name',
        ),
        migrations.AddField(
            model_name='suppliertypebusshelter',
            name='account_number',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypebusshelter',
            name='bank_account_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypebusshelter',
            name='bank_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypebusshelter',
            name='ifsc_code',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypecorporate',
            name='bank_account_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='bank_account_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='bank_account_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='account_number',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='bank_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='account_number',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='bank_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='account_number',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='bank_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='ifsc_code',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]

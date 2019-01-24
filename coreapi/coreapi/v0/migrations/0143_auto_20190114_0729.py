# Generated by Django 2.1.4 on 2019-01-14 07:29

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0142_suppliertypesociety_flat_count_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adinventorylocationmapping',
            name='adinventory_name',
            field=models.CharField(choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner'), ('POSTER LIFT', 'Poster Lift'), ('GLASS_FACADE', 'GLASS_FACADE'), ('HOARDING', 'HOARDING'), ('DROPDOWN', 'DROPDOWN'), ('STANDEE', 'STANDEE'), ('PROMOTION_DESK', 'PROMOTION_DESK'), ('PILLAR', 'PILLAR'), ('TROLLEY', 'TROLLEY'), ('WALL_INVENTORY', 'WALL_INVENTORY'), ('FLOOR_INVENTORY', 'FLOOR_INVENTORY'), ('GATEWAY ARCH', 'GATEWAY ARCH'), ('SUNBOARD', 'SUNBOARD'), ('BANNER', 'BANNER')], db_column='ADINVENTORY_NAME', default='POSTER', max_length=10),
        ),
        migrations.AlterField(
            model_name='adinventorytype',
            name='adinventory_name',
            field=models.CharField(choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner'), ('POSTER LIFT', 'Poster Lift'), ('GLASS_FACADE', 'GLASS_FACADE'), ('HOARDING', 'HOARDING'), ('DROPDOWN', 'DROPDOWN'), ('STANDEE', 'STANDEE'), ('PROMOTION_DESK', 'PROMOTION_DESK'), ('PILLAR', 'PILLAR'), ('TROLLEY', 'TROLLEY'), ('WALL_INVENTORY', 'WALL_INVENTORY'), ('FLOOR_INVENTORY', 'FLOOR_INVENTORY'), ('GATEWAY ARCH', 'GATEWAY ARCH'), ('SUNBOARD', 'SUNBOARD'), ('BANNER', 'BANNER')], db_column='ADINVENTORY_NAME', default='POSTER', max_length=20),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='user_code',
            field=models.CharField(default='0', max_length=255),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='campaigncomments',
            name='inventory_type',
            field=models.CharField(blank=True, choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner'), ('POSTER LIFT', 'Poster Lift'), ('GLASS_FACADE', 'GLASS_FACADE'), ('HOARDING', 'HOARDING'), ('DROPDOWN', 'DROPDOWN'), ('STANDEE', 'STANDEE'), ('PROMOTION_DESK', 'PROMOTION_DESK'), ('PILLAR', 'PILLAR'), ('TROLLEY', 'TROLLEY'), ('WALL_INVENTORY', 'WALL_INVENTORY'), ('FLOOR_INVENTORY', 'FLOOR_INVENTORY'), ('GATEWAY ARCH', 'GATEWAY ARCH'), ('SUNBOARD', 'SUNBOARD'), ('BANNER', 'BANNER')], db_column='inventory_type', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='campaigncomments',
            name='related_to',
            field=models.CharField(blank=True, choices=[('BOOKING', 'BOOKING'), ('EXECUTION', 'EXECUTION')], db_column='related_to', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='corporateparkcompanylist',
            name='name',
            field=models.CharField(blank=True, db_column='COMPANY_NAME', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='emailsettings',
            name='email_type',
            field=models.CharField(choices=[('WEEKLY_LEADS', 'WEEKLY_LEADS'), ('WEEKLY_LEADS_GRAPH', 'WEEKLY_LEADS_GRAPH'), ('BOOKING_DETAILS_BASIC', 'BOOKING_DETAILS_BASIC'), ('BOOKING_DETAILS_ADV', 'BOOKING_DETAILS_ADV')], max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='emailsettings',
            name='user_type',
            field=models.CharField(choices=[('NORMAL', 'NORMAL'), ('ADMIN', 'ADMIN')], default='NORMAL', max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='sunboardinventory',
            name='adinventory_id',
            field=models.CharField(db_column='ADINVENTORY_ID', max_length=22, unique=True),
        ),
        migrations.AlterField(
            model_name='sunboardinventory',
            name='id',
            field=models.AutoField(db_column='ID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='supplierphase',
            name='phase_no',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='flat_count_type',
            field=models.IntegerField(blank=True, choices=[(1, '0-149'), (2, '150-399'), (3, '400+')], null=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='supplier_status',
            field=models.CharField(choices=[('Tapped', 'Tapped'), ('LetterGiven', 'LetterGiven'), ('MeetingRequired', 'MeetingRequired'), ('Other', 'Other')], max_length=80, null=True),
        ),
    ]
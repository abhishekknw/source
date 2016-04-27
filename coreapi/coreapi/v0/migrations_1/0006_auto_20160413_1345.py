# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0005_auto_20160406_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocietyMajorEvents',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('Ganpati', models.BooleanField(default=False, db_column='Ganpati')),
                ('Diwali', models.BooleanField(default=False, db_column='Diwali')),
                ('Lohri', models.BooleanField(default=False, db_column='Lohri')),
                ('Navratri', models.BooleanField(default=False, db_column='Navratri')),
                ('Holi', models.BooleanField(default=False, db_column='Holi')),
                ('Janmashtami', models.BooleanField(default=False, db_column='Janmashtami')),
                ('IndependenceDay', models.BooleanField(default=False, db_column='IndependenceDay')),
                ('RepublicDay', models.BooleanField(default=False, db_column='RepublicDay')),
                ('SportsDay', models.BooleanField(default=False, db_column='SportsDay')),
                ('AnnualDay', models.BooleanField(default=False, db_column='AnnualDay')),
                ('Christmas', models.BooleanField(default=False, db_column='Christmas')),
                ('NewYear', models.BooleanField(default=False, db_column='NewYear')),
                ('past_major_events', models.CharField(max_length=60, null=True, db_column='past_major_events', blank=True)),
                ('supplier', models.ForeignKey(related_name='society_events', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='events',
            name='event_duration',
        ),
        migrations.RemoveField(
            model_name='events',
            name='event_linked',
        ),
        migrations.RemoveField(
            model_name='events',
            name='event_plan_map',
        ),
        migrations.RemoveField(
            model_name='events',
            name='past_major_events',
        ),
        migrations.RemoveField(
            model_name='events',
            name='photograph_1',
        ),
        migrations.RemoveField(
            model_name='events',
            name='photograph_2',
        ),
        migrations.RemoveField(
            model_name='events',
            name='photograph_3',
        ),
        migrations.AddField(
            model_name='events',
            name='end_day',
            field=models.CharField(max_length=30, null=True, db_column='END_DAY', blank=True),
        ),
        migrations.AddField(
            model_name='events',
            name='important_day',
            field=models.CharField(max_length=30, null=True, db_column='IMPORTANT_DAY', blank=True),
        ),
        migrations.AddField(
            model_name='events',
            name='start_day',
            field=models.CharField(max_length=30, null=True, db_column='START_DAY', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_lobby_allowed',
            field=models.BooleanField(default=False, db_column='FLIER_LOBBY_ALLOWED'),
        ),
    ]

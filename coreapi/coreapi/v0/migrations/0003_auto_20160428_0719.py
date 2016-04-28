# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_load_intial_data'),
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
            ],
        ),
        migrations.RemoveField(
            model_name='campaignbookinginfo',
            name='instrument_no',
        ),
        migrations.RemoveField(
            model_name='campaignbookinginfo',
            name='instrument_type',
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
        migrations.RemoveField(
            model_name='inventorysummary',
            name='cd_price_day',
        ),
        migrations.RemoveField(
            model_name='inventorysummary',
            name='stall_price_day',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='sides',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_inventory_status',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_location_in_tower',
        ),
        migrations.AddField(
            model_name='campaignbookinginfo',
            name='payment_mode',
            field=models.CharField(max_length=20, db_column='PAYMENT_MODE', blank=True),
        ),
        migrations.AddField(
            model_name='campaignbookinginfo',
            name='payment_no',
            field=models.CharField(max_length=20, db_column='PAYMENT_NO', blank=True),
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
            name='campaign_count',
            field=models.IntegerField(null=True, db_column='CAMPAIGN_COUNT'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='cd_price_day_premium',
            field=models.IntegerField(null=True, db_column='CD_PRICE_DAY_PREMIUM'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='cd_price_day_standard',
            field=models.IntegerField(null=True, db_column='CD_PRICE_DAY_STANDARD'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_campaign',
            field=models.IntegerField(null=True, db_column='FLIER_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_frequency',
            field=models.IntegerField(null=True, db_column='FLIER_FREQUENCY'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_lobby_allowed',
            field=models.BooleanField(default=False, db_column='FLIER_LOBBY_ALLOWED'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_watchman_allowed',
            field=models.BooleanField(default=False, db_column='FLIER_WATCHMAN_ALLOWED'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='poster_campaign',
            field=models.IntegerField(null=True, db_column='POSTER_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='poster_per_campaign',
            field=models.IntegerField(null=True, db_column='POSTER_PER_CAMPAIGN'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='pricing_confidence',
            field=models.CharField(max_length=20, null=True, db_column='PRICING_CONFIDENCE', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='stall_or_cd_campaign',
            field=models.IntegerField(null=True, db_column='STALL_OR_CD_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='stall_price_day_large',
            field=models.IntegerField(null=True, db_column='STALL_PRICE_DAY_LARGE'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='stall_price_day_small',
            field=models.IntegerField(null=True, db_column='STALL_PRICE_DAY_SMALL'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='standee_campaign',
            field=models.IntegerField(null=True, db_column='STANDEE_CAMPAIGN', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='standee_per_campaign',
            field=models.IntegerField(null=True, db_column='STANDEE_PER_CAMPAIGN'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='age_of_society',
            field=models.FloatField(null=True, db_column='AGE_OF_SOCIETY', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_count',
            field=models.BooleanField(default=True, db_column='SOCIETY_COUNT'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_off',
            field=models.BooleanField(default=False, db_column='SOCIETY_OFF'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_ratings',
            field=models.BooleanField(default=True, db_column='SOCIETY_RATINGS'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='total_campaign',
            field=models.IntegerField(null=True, db_column='TOTAL_CAMPAIGN', blank=True),
        ),
        migrations.AlterField(
            model_name='campaignbookinginfo',
            name='booking_amount',
            field=models.FloatField(null=True, db_column='BOOKING_AMOUNT'),
        ),
        migrations.AlterField(
            model_name='noticeboarddetails',
            name='notice_board_size_length',
            field=models.FloatField(default=0.0, null=True, db_column='NOTICE_BOARD_SIZE_LENGTH', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='bachelor_tenants_allowed',
            field=models.CharField(max_length=5, null=True, db_column='BACHELOR_TENANTS_ALLOWED'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_campaign_occurred',
            field=models.CharField(max_length=5, null=True, db_column='PAST_CAMPAIGN_OCCURRED'),
        ),
        migrations.AddField(
            model_name='societymajorevents',
            name='supplier',
            field=models.ForeignKey(related_name='society_events', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True),
        ),
    ]

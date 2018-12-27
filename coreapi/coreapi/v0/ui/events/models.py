from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from v0.ui.base.models import BaseModel
from v0.constants import supplier_id_max_length
from v0 import managers

class SocietyMajorEvents(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='society_events', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    Ganpati = models.BooleanField(db_column='Ganpati', default=False)
    Diwali = models.BooleanField(db_column='Diwali', default=False)
    Lohri = models.BooleanField(db_column='Lohri', default=False)
    Navratri = models.BooleanField(db_column='Navratri', default=False)
    Holi = models.BooleanField(db_column='Holi', default=False)
    Janmashtami = models.BooleanField(db_column='Janmashtami', default=False)
    IndependenceDay = models.BooleanField(db_column='IndependenceDay', default=False)
    RepublicDay = models.BooleanField(db_column='RepublicDay', default=False)
    SportsDay = models.BooleanField(db_column='SportsDay', default=False)
    AnnualDay = models.BooleanField(db_column='AnnualDay', default=False)
    Christmas = models.BooleanField(db_column='Christmas', default=False)
    NewYear = models.BooleanField(db_column='NewYear', default=False)
    past_major_events = models.IntegerField(db_column='PAST_MAJOR_EVENTS', blank=True, null=True)

class Events(models.Model):
    event_id = models.AutoField(db_column='EVENT_ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='events', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    event_name = models.CharField(db_column='EVENT_NAME', max_length=20, blank=True, null=True)
    event_location = models.CharField(db_column='EVENT_LOCATION', max_length=50, blank=True, null=True)
    past_gathering_per_event = models.IntegerField(db_column='PAST_GATHERING_PER_EVENT', blank=True, null=True)
    start_day = models.CharField(db_column='START_DAY', max_length=30, blank=True, null=True)
    end_day = models.CharField(db_column='END_DAY', max_length=30, blank=True, null=True)
    important_day = models.CharField(db_column='IMPORTANT_DAY', max_length=30, blank=True, null=True)
    activities = models.CharField(db_column='ACTIVITIES', max_length=50, blank=True, null=True)
    stall_spaces_count = models.IntegerField(db_column='STALL_SPACES_COUNT', blank=True, null=True)
    banner_spaces_count = models.IntegerField(db_column='BANNER_SPACES_COUNT', blank=True, null=True)
    poster_spaces_count = models.IntegerField(db_column='POSTER_SPACES_COUNT', blank=True, null=True)
    standee_spaces_count = models.IntegerField(db_column='STANDEE_SPACES_COUNT', blank=True, null=True)
    event_status = models.CharField(db_column='EVENT_STATUS', max_length=10, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:

        db_table = 'events'
from django.db import models
from django.conf import settings
from v0.models import BaseModel, managers, fields

class RatioDetails(models.Model):
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=20)  # Field name made lowercase.
    machadalo_index = models.CharField(db_column='MACHADALO_INDEX', max_length=30)  # Field name made lowercase.
    age_proportions = models.CharField(db_column='AGE_PROPORTIONS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    flat_avg_rental_persqft = models.CharField(db_column='FLAT_AVG_RENTAL_PERSQFT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    flat_avg_size = models.CharField(db_column='FLAT_AVG_SIZE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    flat_sale_cost_persqft = models.CharField(db_column='FLAT_SALE_COST_PERSQFT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_count = models.IntegerField(db_column='WALL_COUNT', blank=True, null=True)  # Field name made lowercase.
    major_event_count = models.IntegerField(db_column='MAJOR_EVENT_COUNT', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'ratio_details'
        unique_together = (('supplier_id', 'machadalo_index'),)

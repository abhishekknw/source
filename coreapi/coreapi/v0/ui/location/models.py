from django.db import models
from v0.ui.base.models import BaseModel
from v0.constants import supplier_id_max_length
from django.contrib.contenttypes import fields
from v0 import managers
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class State(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    state_name = models.CharField(db_column='STATE_NAME', max_length=50, null=True)
    state_code = models.CharField(db_column='STATE_CODE', max_length=5, null=True)

    class Meta:

        db_table = 'state'

class City(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    city_name = models.CharField(db_column='CITY_NAME', max_length=100, null=True)
    city_code = models.CharField(db_column='CITY_CODE', max_length=5, null=True)
    state_code = models.ForeignKey(State, related_name='statecode', db_column='STATE_CODE', null=True, on_delete=models.CASCADE)

    class Meta:

        db_table = 'city'
        # a city can only contain unique state_codes
        unique_together = (('state_code','city_code'),)


class CityArea(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    label = models.CharField(db_column='AREA_NAME', max_length=100, null=True)
    area_code = models.CharField(db_column='AREA_CODE', max_length=5, null=True)
    city_code = models.ForeignKey(City, related_name='citycode', db_column='CITY_CODE', null=True, on_delete=models.CASCADE)

    class Meta:

        db_table = 'city_area'
        unique_together = (('area_code','city_code'),)


class CitySubArea(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    subarea_name = models.CharField(db_column='SUBAREA_NAME', max_length=100, null=True)
    subarea_code = models.CharField(db_column='SUBAREA_CODE', max_length=5, null=True)
    locality_rating = models.CharField(db_column='LOCALITY_RATING', max_length=100, null=True)
    area_code = models.ForeignKey(CityArea, related_name='areacode', db_column='AREA_CODE', null=True,on_delete=models.CASCADE)

    class Meta:

        db_table = 'city_area_subarea'
        unique_together = (('area_code','subarea_code'),)

class ImageMapping(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    location_id = models.CharField(db_column='LOCATION_ID', max_length=20, blank=True, null=True)
    location_type = models.CharField(db_column='LOCATION_TYPE', max_length=20, blank=True, null=True)
    supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='images', blank=True, null=True, on_delete=models.CASCADE)
    image_url = models.CharField(db_column='IMAGE_URL', max_length=100)
    comments = models.CharField(db_column='COMMENTS', max_length=100, blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'image_mapping'

class ShortlistedSpacesVersion(models.Model):
    space_mapping_version   = models.ForeignKey('SpaceMappingVersion',db_index=True, related_name='spaces_version',on_delete=models.CASCADE)
    supplier_code   = models.CharField(max_length=4)
    content_type    = models.ForeignKey(ContentType, related_name='spaces_version')
    object_id       = models.CharField(max_length=12)
    content_object  = fields.GenericForeignKey('content_type', 'object_id')
    buffer_status   = models.BooleanField(default=False)

    class Meta:
        #db_table = 'SHORTLISTED_SPACES_VERSION'
        db_table = 'shortlisted_spaces_version'

class ShortlistedSpaces(BaseModel):
    """
    This model stores all the shortlisted spaces. One Supplier or space can be under different campaigns.
    in one campaign it's status can be removed while in the other it's buffered. Hence this model is made
    for mapping such relations.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    space_mapping = models.ForeignKey('SpaceMapping', db_index=True, related_name='spaces', on_delete=models.CASCADE, null=True, blank=True)
    center = models.ForeignKey('ProposalCenterMapping', null=True, blank=True)
    proposal = models.ForeignKey('ProposalInfo', null=True, blank=True)
    supplier_code = models.CharField(max_length=4, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, related_name='spaces')
    object_id = models.CharField(max_length=supplier_id_max_length)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    buffer_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, null=True, blank=True)
    objects = managers.GeneralManager()
    campaign_status = models.CharField(max_length=10, default='', null=True, blank=True)
    phase = models.CharField(max_length=10, default='',  null=True, blank=True)
    payment_status = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    total_negotiated_price = models.CharField(max_length=255, null=True, blank=True)
    booking_status = models.CharField(max_length=10, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
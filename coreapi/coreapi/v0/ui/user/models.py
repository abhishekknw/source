from v0 import managers
from django.conf import settings
from django.db import models
from v0.ui.location.models import City, CityArea


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID,  unique=True, editable=True, null=False, related_name='user_profile', db_column='user_id', on_delete=models.CASCADE)
    is_city_manager = models.BooleanField(db_column='is_city_manager', default=False)
    is_cluster_manager = models.BooleanField(db_column='is_cluster_manager', default=False)
    is_normal_user = models.BooleanField(db_column='is_normal_user', default=False)
    society_form_access = models.BooleanField(db_column='society_form_access', default=False)
    corporate_form_access = models.BooleanField(db_column='corporate_form_access', default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, db_column='created_by', null=True, on_delete=models.CASCADE)
    objects = managers.GeneralManager()

    def get_user(self):
        return self.user

    class Meta:
        db_table = 'user_profile'


class UserCities(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID,  related_name='cities', db_column='user_id', null=False, on_delete=models.CASCADE)
    city = models.ForeignKey(City, db_column='city_id', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_cities'


class UserAreas(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, related_name='clusters', db_column='user_id', null=False, on_delete=models.CASCADE)
    area = models.ForeignKey(CityArea, db_column='area_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_areas'

class UserInquiry(models.Model):
    inquiry_id = models.AutoField(db_column='INQUIRY_ID', primary_key=True)
    company_name = models.CharField(db_column='COMPANY_NAME', max_length=40)
    contact_person_name = models.CharField(db_column='CONTACT_PERSON_NAME', max_length=40, blank=True, null=True)
    email = models.CharField(db_column='EMAIL', max_length=40, blank=True, null=True)
    phone = models.IntegerField(db_column='PHONE', blank=True, null=True)
    inquiry_details = models.TextField(db_column='INQUIRY_DETAILS')

    class Meta:

        db_table = 'user_inquiry'
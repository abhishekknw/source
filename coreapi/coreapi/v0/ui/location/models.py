from django.db import models

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
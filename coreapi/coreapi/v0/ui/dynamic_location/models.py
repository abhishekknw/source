from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields


class StateDetails(MongoModel):
    state_name = fields.CharField()
    state_code = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'

class CityDetails(MongoModel):
    city_name = fields.CharField()
    city_code = fields.CharField()
    state_code = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'

class CityAreaDetails(MongoModel):
    label = fields.CharField()
    area_code = fields.CharField()
    city_code = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'

class CitySubAreaDetails(MongoModel):
    subarea_name = fields.CharField()
    subarea_code = fields.CharField()
    locality_rating = fields.CharField()
    area_code = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

connect("mongodb://localhost:27017/machadalo", alias="mongo_app")


class SupplyEntityType(MongoModel):
    name = fields.CharField()
    entity_attributes = fields.ListField()
    organisation_id = fields.CharField()
    created_by = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
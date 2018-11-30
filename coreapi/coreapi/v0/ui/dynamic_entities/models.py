from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

connect("mongodb://localhost:27017/machadalo", alias="mongo_app")


class SupplyEntityType(MongoModel):
    name = fields.CharField()
    entity_attributes = fields.ListField()
    is_global = fields.BooleanField()
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class SupplyEntity(MongoModel):
    '''
    entity_attributes: list of dicts, which looks like this:
        "entity_attributes":[{"name":"latitude","type":"Float", "value":12.9803195},{"name":"longitude","type":"Float",
        "value": 77.7509302},{"name":"area", "type":"String", "value":"Whitefield"}, {"name":"pincode", "type":"Integer",
        "value":560066},{"name": "locality", "type":"String", "value":"Channasandra"},
        {"name":"inventories", "type":"InventoryList", "value":[]}]
    '''
    name = fields.CharField()
    entity_type_id = fields.CharField()  # This should be present in entity_type fields
    is_custom = fields.BooleanField(default=False)  # are there any new attributes not present in SupplyEntityType?
    entity_attributes = fields.ListField()
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
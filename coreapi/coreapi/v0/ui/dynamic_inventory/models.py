from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

connect("mongodb://localhost:27017/machadalo", alias="mongo_app")


class BaseInventory(MongoModel):
    '''
    entity_attributes: list of dicts, which looks like this:
        "entity_attributes":[{"name":"latitude","type":"Float", "value":12.9803195},{"name":"longitude","type":"Float",
        "value": 77.7509302},{"name":"area", "type":"String", "value":"Whitefield"}, {"name":"pincode", "type":"Integer",
        "value":560066},{"name": "locality", "type":"String", "value":"Channasandra"},
        {"name":"inventories", "type":"InventoryList", "value":[]}]
    '''
    name = fields.CharField()
    is_global = fields.BooleanField(default=False)
    inventory_type = fields.CharField()  # Time based, Frequency Based, Space Based
    base_attributes = fields.ListField()  # latitude, longitude, frequency, duration, height, width, etc.
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    supplier_id = fields.CharField()  # This can be changed to entity_id
    campaign_id = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class Inventory(MongoModel):
    '''
    entity_attributes: list of dicts, which looks like this:
        "entity_attributes":[{"name":"latitude","type":"Float", "value":12.9803195},{"name":"longitude","type":"Float",
        "value": 77.7509302},{"name":"area", "type":"String", "value":"Whitefield"}, {"name":"pincode", "type":"Integer",
        "value":560066},{"name": "locality", "type":"String", "value":"Channasandra"},
        {"name":"inventories", "type":"InventoryList", "value":[]}]
    '''
    name = fields.CharField()
    is_global = fields.BooleanField(default=False)
    base_inventory = fields.CharField()
    inventory_attributes = fields.ListField()  # latitude, longitude, frequency, duration, height, width, etc.
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    supplier_id = fields.CharField()  # This can be changed to entity_id
    campaign_id = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
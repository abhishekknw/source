from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields


class BaseInventory(MongoModel):
    '''
        {"name":"Poster", "supplier_id":"MUMAECKRSHD3", "campaign_id":"HDFHDF0789",
        "base_attributes":[{"name":"latitude","type": "FLOAT"}, {"name":"longitude","type": "FLOAT"},
        {"name":"height","type":"FLOAT"}, {"name":"width","type":"FLOAT"}], "inventory_type": "space_based"
        }
    '''
    name = fields.CharField()
    is_global = fields.BooleanField(default=False)
    inventory_type = fields.CharField()  # Time based, Frequency Based, Space Based
    base_attributes = fields.ListField()  # latitude, longitude, frequency, duration, height, width, etc.
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class Inventory(MongoModel):
    name = fields.CharField()
    is_global = fields.BooleanField(default=False)
    base_inventory = fields.CharField()
    inventory_attributes = fields.ListField()  # latitude, longitude, frequency, duration, height, width, etc.
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
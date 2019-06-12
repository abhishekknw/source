from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields


class SupplySupplierType(MongoModel):
    name = fields.CharField()
    supplier_attributes = fields.ListField()
    inventory_list = fields.ListField() # Inventory objects with pricing details
    additional_attributes = fields.OrderedDictField()
    is_global = fields.BooleanField()
    base_supplier_type_id = fields.CharField()  # id of the base supplier type
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class SupplySupplier(MongoModel):
    '''
    supplier_attributes: list of dicts, which looks like this:
        "supplier_attributes":[{"name":"latitude","type":"Float", "value":12.9803195},{"name":"longitude","type":"Float",
        "value": 77.7509302},{"name":"area", "type":"String", "value":"Whitefield"}, {"name":"pincode", "type":"Integer",
        "value":560066},{"name": "locality", "type":"String", "value":"Channasandra"},
        {"name":"inventories", "type":"InventoryList", "value":[]}]
    '''
    name = fields.CharField()
    supplier_type_id = fields.CharField()  # This should be present in supplier_type fields
    old_supplier_id = fields.CharField(blank=True)
    is_custom = fields.BooleanField(default=False)  # are there any new attributes not present in SupplySupplierType?
    supplier_attributes = fields.ListField()
    inventory_list = fields.ListField() # Inventory objects with pricing details
    additional_attributes = fields.OrderedDictField()
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class BaseSupplySupplierType(MongoModel):
    name = fields.CharField()
    supplier_attributes = fields.ListField()
    inventory_list = fields.ListField()  # Inventory objects with pricing details
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
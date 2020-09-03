from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from django.conf import settings


class ChecklistPermissions(MongoModel):
    profile_id = fields.IntegerField()
    organisation_id = fields.CharField()
    checklist_permissions = fields.ListField()  # CREATE, UPDATE, READ, DELETE, FREEZE, UNFREEZE, FILL
    allowed_campaigns = fields.ListField()  #  All if empty
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class ChecklistData(MongoModel):
    status = fields.CharField()
    supplier_id = fields.CharField()
    order_id = fields.IntegerField()
    campaign_id = fields.CharField()
    checklist_id = fields.IntegerField()
    rowid = fields.IntegerField()
    created_at = fields.DateTimeField()
    data = fields.DictField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class ChecklistOperators(MongoModel):
    status = fields.CharField()
    operator_id = fields.IntegerField()
    checklist_id = fields.IntegerField()
    column_ids = fields.ListField()
    column_operations = fields.DictField()
    result_operations = fields.ListField()
    operator_name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
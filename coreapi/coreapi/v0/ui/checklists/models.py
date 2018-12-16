from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

connect("mongodb://localhost:27017/machadalo", alias="mongo_app")


class ChecklistPermissions(MongoModel):
    user_id = fields.IntegerField()
    organisation_id = fields.CharField()
    profile_id = fields.IntegerField()
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
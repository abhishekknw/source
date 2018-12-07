from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

connect("mongodb://localhost:27017/machadalo", alias="mongo_app")


class Notifications(MongoModel):
    to_id = fields.IntegerField()
    from_id = fields.IntegerField()
    notification_msg = fields.CharField()
    is_read = fields.BooleanField(default=False)
    last_read_timestamp = fields.DateTimeField()
    organisation_id = fields.CharField()
    module_name = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
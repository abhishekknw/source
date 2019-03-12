from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

connect("mongodb://localhost:27017/machadalo", alias="mongo_app")


class BaseBookingTemplate(MongoModel):
    name = fields.CharField()
    base_entity_type_id = fields.CharField()
    organisation_id = fields.CharField()
    booking_attributes = fields.ListField()
    entity_attributes = fields.ListField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class BookingTemplate(MongoModel):
    name = fields.CharField()
    base_booking_template_id = fields.CharField()
    entity_type_id = fields.CharField()
    organisation_id = fields.CharField()
    booking_attributes = fields.ListField()
    entity_attributes = fields.ListField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
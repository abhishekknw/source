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


class BookingData(MongoModel):
    booking_template_id = fields.CharField()
    campaign_id = fields.CharField()
    entity_id = fields.CharField()
    organisation_id = fields.CharField()
    booking_attributes = fields.ListField()
    comments = fields.ListField()
    inventory_counts = fields.ListField()
    phase_id = fields.IntegerField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class BookingDetails(MongoModel):
    booking_template_id = fields.CharField()
    campaign_id = fields.CharField()
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class BookingInventoryActivity(MongoModel):
    entity_id = fields.CharField()
    campaign_id = fields.CharField()
    assigned_to_id = fields.CharField()
    activity_type = fields.CharField()  # RELEASE or AUDIT or CLOSURE
    inventory_name = fields.CharField()  # POSTER or STALL or STANDEE
    activity_date = fields.DateTimeField()
    actual_activity_date = fields.DateTimeField()
    status = fields.CharField()
    comments = fields.ListField()
    inventory_images = fields.ListField()
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'



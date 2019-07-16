from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields


class BaseBookingTemplate(MongoModel):
    name = fields.CharField()
    base_supplier_type_id = fields.CharField()
    organisation_id = fields.CharField()
    booking_attributes = fields.ListField()
    supplier_attributes = fields.ListField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class BookingTemplate(MongoModel):
    name = fields.CharField()
    base_booking_template_id = fields.CharField()
    supplier_type_id = fields.CharField()
    organisation_id = fields.CharField()
    booking_attributes = fields.ListField()
    supplier_attributes = fields.ListField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class BookingData(MongoModel):
    booking_template_id = fields.CharField()
    campaign_id = fields.CharField()
    supplier_id = fields.CharField()
    organisation_id = fields.CharField()
    booking_attributes = fields.ListField()
    comments = fields.ListField()
    inventory_counts = fields.ListField()
    phase_id = fields.IntegerField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    user_id = fields.IntegerField()
    center_id = fields.IntegerField()
    supplier_id_old = fields.CharField()

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


class BookingInventory(MongoModel):
    supplier_id = fields.CharField()
    campaign_id = fields.CharField()
    inventory_name = fields.CharField()  # POSTER or STALL or STANDEE
    comments = fields.ListField(blank=True)
    inventory_images = fields.ListField(blank=True)
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    supplier_id_old = fields.CharField()
    inventory_id_old = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class BookingInventoryActivity(MongoModel):
    booking_inventory_id = fields.CharField()
    inventory_name = fields.CharField()
    supplier_id = fields.CharField()
    campaign_id = fields.CharField()
    assigned_to_id = fields.CharField(blank=True)
    activity_type = fields.CharField()  # RELEASE or AUDIT or CLOSURE
    activity_date = fields.DateTimeField()
    actual_activity_date = fields.DateTimeField()
    status = fields.CharField(blank=True)
    comments = fields.ListField(blank=True)
    inventory_images = fields.ListField(blank=True)
    organisation_id = fields.CharField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'



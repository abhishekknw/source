from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields


class ResidentDetail(MongoModel):
    name = fields.CharField()
    contact_number = fields.CharField()
    alternate_contact_number = fields.ListField()
    details = fields.DictField()  # society_name, society_id, type_of_flat, flat_number, tower_number, address
    comments = fields.ListField()
    is_active = fields.BooleanField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    updated_by = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class User(MongoModel):
    name = fields.CharField()
    contact_number = fields.ListField()
    residence_details = fields.ListField()
    children_details = fields.ListField()
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    updated_by = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class ResidentCampaignDetail(MongoModel):
    message_id = fields.CharField()
    contact_number = fields.CharField()
    campaign_id = fields.CharField()
    lead_phases = fields.DictField()     # impression, click, lead, hot_lead ,in_between, converted
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    updated_by = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
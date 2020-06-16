from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields


class User(MongoModel):
    name = fields.CharField()                   # parent name
    contact_number = fields.IntegerField()
    alternate_contact_number = fields.IntegerField()
    children_details = fields.ListField()       # [{name: '', class: '' , school: ''}, {name: '', class: '', school: ''}]
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class ResidentDetail(MongoModel):
    name = fields.CharField()               # user name
    user_id = fields.CharField()
    society_details = fields.ListField()  # [{society_name, society_id, type_of_flat, flat_number, tower_number, address}]
    comments = fields.ListField()
    is_active = fields.BooleanField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class ResidentCampaignDetail(MongoModel):
    message_id = fields.CharField()
    user_id = fields.CharField()            # Store user -> _id here
    resident_id = fields.CharField()       # Store resident -> _id here
    campaign_id = fields.CharField()
    lead_phases = fields.DictField()     # impression, click, lead, hot_lead ,in_between, converted
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
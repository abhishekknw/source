from django.db import models
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from django.conf import settings

class Gupshup(MongoModel):
    data = fields.CharField(blank=True)
    created_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'

class ContactVerification(MongoModel):
    mobile = fields.CharField(blank=True)
    name = fields.CharField(blank=True)
    designation = fields.CharField(blank=True)
    entity_name = fields.CharField(blank=True)
    mobile = fields.CharField(blank=True)
    verification_status = fields.ListField(blank=True)
    user_status = fields.ListField(blank=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'

class MessageTemplate(models.Model):
    verification_status = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'gupshup_message'


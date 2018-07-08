from django.db import models
from v0.ui.base.models import BaseModel
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from v0 import managers
from v0.ui.account.models import BusinessAccountContact

# five possible organization types
ORGANIZATION_CATEGORY = (
    ('MACHADALO', 'MACHADALO'),
    ('BUSINESS', 'BUSINESS'),
    ('BUSINESS_AGENCY', 'BUSINESS_AGENCY'),
    ('SUPPLIER_AGENCY', 'SUPPLIER_AGENCY'),
    ('SUPPLIER', 'SUPPLIER')
)


class Organisation(BaseModel):
    """
    This is model which captures the essence of any organisation interacting with our system. The class
    Business is merly a type of this model and will be soon be deleted once, the data is migrated into this model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    organisation_id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    type_name = models.ForeignKey('BusinessTypes', null=True, blank=True)
    sub_type = models.ForeignKey('BusinessSubTypes', null=True, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    email = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    reference_name = models.CharField(max_length=50, blank=True)
    reference_phone = models.CharField(max_length=10, blank=True)
    reference_email = models.CharField(max_length=50, blank=True)
    comments = models.TextField(max_length=100, blank=True)
    contacts = GenericRelation(BusinessAccountContact)
    category = models.CharField(max_length=30, choices=ORGANIZATION_CATEGORY, default=ORGANIZATION_CATEGORY[1][0])
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'organisation'



class OrganisationMap(BaseModel):
    """
    Generic table that maps relationship between any two organisations.
    """
    first_organisation = models.ForeignKey(Organisation, related_name='first_organisation')
    second_organisation = models.ForeignKey(Organisation, related_name='second_organisation')

    class Meta:
        db_table = 'organisation_map'

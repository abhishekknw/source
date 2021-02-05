from django.db import models
from v0.ui.base.models import BaseModel
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from v0 import managers
from v0.ui.account.models import BusinessAccountContact, BusinessTypes, BusinessSubTypes
from v0.ui.common.models import mongo_client
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organisation_id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    type_name = models.ForeignKey('BusinessTypes', null=True, blank=True, on_delete=models.CASCADE, related_name='company')
    sub_type = models.ForeignKey('BusinessSubTypes', null=True, blank=True, on_delete=models.CASCADE, related_name='company_subtype')
    business_type = models.ManyToManyField(BusinessTypes)
    business_subtype = models.ManyToManyField(BusinessSubTypes)
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
    created_by_org = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    gstin = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    billing_address = models.CharField(max_length=100, blank=True, null=True)
    pan_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'organisation'
    
    def save(self, *args, **kwargs):
        mongo_client.api_cache.remove({"slugType": 'organisation'})
        super(Organisation, self).save(*args, **kwargs)

class OrganisationMap(BaseModel):
    """
    Generic table that maps relationship between any two organisations.
    """
    first_organisation = models.ForeignKey(Organisation, related_name='first_organisation', on_delete=models.CASCADE)
    second_organisation = models.ForeignKey(Organisation, related_name='second_organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'organisation_map'

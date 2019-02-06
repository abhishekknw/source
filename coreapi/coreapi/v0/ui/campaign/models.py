from django.conf import settings
from django.db import models
from v0.ui.base.models import BaseModel
from v0.ui.account.models import AccountInfo
from v0.ui.inventory.models import SupplierTypeSociety, SocietyInventoryBooking
from v0.ui.proposal.models import ProposalInfo
from v0.ui.common.models import BaseUser
from django.core.exceptions import ObjectDoesNotExist
from v0 import managers
from v0.ui.inventory.models import AD_INVENTORY_CHOICES


class CampaignTypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    type_name = models.CharField(db_column='TYPE_NAME', max_length=20, blank=True) #change to enum

    class Meta:
        db_table = 'campaign_types'


class Campaign(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    #campaign_type = models.ForeignKey(CampaignTypes, related_name='campaigns', db_column='CAMPAIGN_TYPE_ID', null=True)
    account = models.ForeignKey(AccountInfo, related_name='campaigns', db_column='BUSINESS_ID', null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(db_column='START_DATE', null=True)
    end_date = models.DateTimeField(db_column='END_DATE', null=True)
    tentative_cost = models.IntegerField(db_column='TENTATIVE_COST', null=True)
    booking_status = models.CharField(db_column='BOOKING_STATUS', max_length=20, blank=True) #change to enum

    def __str__(self):
        return self.account.name

    def __unicode__(self):
        return self.account.name

    def get_types(self):
        # CampaignTypeMapping Model
        try:
            return self.types.all()
        except:
            return None

    def get_society_count(self):
        try:
            return self.societies.all().count()
        except:
            return None

    def get_info(self):
        info = {}
        flats = 0
        residents = 0
        ad_spaces = 0
        try:
            societies = self.societies.all()
            for key in societies:
                flats += key.society.flat_count
                residents += key.society.resident_count
                if key.society.total_ad_spaces is not None:
                    ad_spaces += key.society.total_ad_spaces

            info['flat_count'] = flats
            info['resident_count'] = residents
            info['ad_spaces'] = ad_spaces

            return info

        except:
            return {}

    class Meta:

        db_table = 'campaign'

#Need to remove
class CampaignSupplierTypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    campaign = models.ForeignKey(Campaign, related_name='supplier_types', db_column='CAMPAIGN_ID', null=True, on_delete=models.CASCADE)
    supplier_type = models.CharField(db_column='SUPPLIER_TYPE', max_length=20, blank=True) #change to enum
    count = models.IntegerField(db_column='COUNT', null=True)


    class Meta:

        db_table = 'campaign_supplier_types'

#Need to remove
class CampaignTypeMapping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    campaign = models.ForeignKey(Campaign, related_name='types', db_column='CAMPAIGN_ID', null=True, on_delete=models.CASCADE)
    type = models.CharField(db_column='TYPE', max_length=20, blank=True) #change to enum
    sub_type = models.CharField(db_column='SUB_TYPE', max_length=20, blank=True)


    class Meta:

        db_table = 'campaign_type_mapping'


class CampaignSocietyMapping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    campaign = models.ForeignKey(Campaign, related_name='societies', db_column='CAMPAIGN_ID', null=True, on_delete=models.CASCADE)
    society = models.ForeignKey(SupplierTypeSociety, related_name='campaigns', db_column='SUPPLIER_ID', null=True, on_delete=models.CASCADE)
    booking_status = models.CharField(db_column='BOOKING_STATUS', max_length=20, blank=True) #change to enum
    adjusted_price = models.IntegerField(db_column='ADJUSTED_PRICE', null=True)
    comments = models.TextField(db_column='COMMENTS',  max_length=100, blank=True)


    def get_inventories(self):
        try:
            return SocietyInventoryBooking.objects.filter(campaign=self.campaign, society=self.society)
        except:
            return None

    def get_campaign(self):
        try:
            return self.campaign
        except:
            return None

    def get_society(self):
        try:
            return self.society
        except:
            return None

    class Meta:

        db_table = 'campaign_society_mapping'

class CampaignAssignment(BaseModel):
    """
    The model to store a particular campaign being assigned to a user
    """
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='assigned_by', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='assigned_to', on_delete=models.CASCADE)
    campaign = models.ForeignKey(ProposalInfo, null=False, blank=False, on_delete=models.CASCADE)
    # possible primary key should be campaign_id

    class Meta:
        db_table = 'campaign_assignment'


class GenericExportFileName(BaseModel):
    """
    This model stores file name generated by GenericExport API.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    business = models.ForeignKey('BusinessInfo', null=True, blank=True, on_delete=models.CASCADE)
    organisation = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    account = models.ForeignKey('AccountInfo', null=True, blank=True, on_delete=models.CASCADE)
    proposal = models.ForeignKey('ProposalInfo', null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=1000, null=True, blank=True)
    is_exported = models.BooleanField(default=True)
    objects = managers.GeneralManager()

    @property
    def calculate_assignment_detail(self):
        """
        This method is a property which just calculates to whom this proposal was being assigned while converting it to a
        campaign. This can be used as a field in a serializer class.
        """
        try:
            instance = CampaignAssignment.objects.filter(campaign=self.proposal).all()
            if len(instance) > 0:
                instance = instance[0]
            else:
                raise ObjectDoesNotExist
            # can use caching here to avoid BaseUser calls.
            return {
                'assigned_by': BaseUser.objects.get(pk=instance.assigned_by.pk).username,
                'assigned_to': BaseUser.objects.get(pk=instance.assigned_to.pk).username
            }
        except ObjectDoesNotExist:
            return {
                'assigned_by': 'Nobody',
                'assigned_to': 'Nobody'
            }

    class Meta:
        db_table = 'generic_export_file_name'


class CampaignComments(BaseModel):
    RELATED_TO_CHOICES = (
        ('BOOKING', 'BOOKING'),
        ('EXECUTION', 'EXECUTION')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True, blank=True)
    campaign_id = models.CharField(db_index=True, max_length=70, null=True, blank=True)
    shortlisted_spaces = models.ForeignKey('ShortlistedSpaces', null=False, blank=False, on_delete=models.CASCADE)
    inventory_type = models.CharField(db_column='inventory_type', max_length=20,
                                        choices=AD_INVENTORY_CHOICES, null=True, blank=True)
    related_to = models.CharField(db_column='related_to', max_length=20,
                                        choices=RELATED_TO_CHOICES, null=True, blank=True)
    class Meta:
        db_table = 'campaign_comments'
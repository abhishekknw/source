from django.conf import settings
from django.db import models
from v0 import managers
from django.contrib.contenttypes.models import ContentType
from v0.ui.base.models import BaseModel
#from v0.models import SpaceMapping, SpaceMappingVersion

class ProposalCenterMapping(BaseModel):
    """
    for a given proposal, stores lat, long, radius, city, pincode etc.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    proposal    = models.ForeignKey('ProposalInfo', db_index=True, related_name='centers', on_delete=models.CASCADE)
    center_name = models.CharField(max_length=50)
    address     = models.CharField(max_length=150,null=True, blank=True)
    latitude    = models.FloatField(default=0.0)
    longitude   = models.FloatField(default=0.0)
    radius      = models.FloatField(default=0.0)
    subarea     = models.CharField(max_length=35)
    area        = models.CharField(max_length=35)
    city        = models.CharField(max_length=35)
    pincode     = models.IntegerField()
    objects = managers.GeneralManager()

    def get_space_mappings(self):
        return SpaceMapping.objects.get(center=self)

    class Meta:
        db_table = 'proposal_center_mapping'
        unique_together = (('proposal','center_name'),)

class ProposalCenterMappingVersion(models.Model):
    proposal_version    = models.ForeignKey("ProposalInfoVersion", db_index=True, related_name='centers_version', on_delete=models.CASCADE)
    center_name = models.CharField(max_length=50)
    address     = models.CharField(max_length=150, null=True, blank=True)
    latitude    = models.FloatField()
    longitude   = models.FloatField()
    radius      = models.FloatField()
    subarea     = models.CharField(max_length=35, default='')
    area        = models.CharField(max_length=35, default='')
    city        = models.CharField(max_length=35, default='')
    pincode     = models.IntegerField(default=0)

    def get_space_mappings_versions(self):
        return SpaceMappingVersion.objects.get(center_version=self)

    class Meta:
        db_table = 'proposal_center_mapping_version'
        unique_together = (('proposal_version','center_name'),)

class SpaceMapping(models.Model):
    """
    This model talks about what spaces or suppliers are allowed or not at a center for a given proposal.
    """
    center              = models.OneToOneField(ProposalCenterMapping,db_index=True, related_name='space_mappings', on_delete=models.CASCADE)
    proposal            = models.ForeignKey('ProposalInfo', related_name='space_mapping', on_delete=models.CASCADE)
    society_allowed     = models.BooleanField(default=False)
    society_count       = models.IntegerField(default=0)
    society_buffer_count = models.IntegerField(default=0)
    corporate_allowed   = models.BooleanField(default=False)
    corporate_count     = models.IntegerField(default=0)
    corporate_buffer_count = models.IntegerField(default=0)
    gym_allowed         = models.BooleanField(default=False)
    gym_count           = models.IntegerField(default=0)
    gym_buffer_count    = models.IntegerField(default=0)
    salon_allowed      = models.BooleanField(default=False)
    salon_count        = models.IntegerField(default=0)
    salon_buffer_count = models.IntegerField(default=0)

    def get_all_inventories(self):
        return self.inventory_types.all()

    def get_society_inventories(self):
        return self.inventory_types.get(supplier_code='RS')

    def get_corporate_inventories(self):
        return self.inventory_types.get(supplier_code='CP')

    def get_gym_inventories(self):
        return self.inventory_types.get(supplier_code='GY')

    def get_salon_inventories(self):
        return self.inventory_types.get(supplier_code='SA')

    def get_all_spaces(self):
        return self.spaces.all()

    def get_societies(self):
        return self.spaces.filter(supplier_code='RS')

    def get_corporates(self):
        return self.spaces.filter(supplier_code='CP')

    def get_gyms(self):
        return self.spaces.filter(supplier_code='GY')

    def get_salons(self):
        return self.spaces.filter(supplier_code='SA')

    class Meta:
        #db_table = 'SPACE_MAPPING'
        db_table = 'space_mapping'

class SpaceMappingVersion(models.Model):
    center_version      = models.OneToOneField(ProposalCenterMappingVersion,db_index=True, related_name='space_mappings_version', on_delete=models.CASCADE)
    proposal_version    = models.ForeignKey('ProposalInfoVersion', related_name='space_mapping_version', on_delete=models.CASCADE)
    society_allowed     = models.BooleanField(default=False)
    society_count       = models.IntegerField(default=0)
    society_buffer_count = models.IntegerField(default=0)
    corporate_allowed   = models.BooleanField(default=False)
    corporate_count     = models.IntegerField(default=0)
    corporate_buffer_count = models.IntegerField(default=0)
    gym_allowed         = models.BooleanField(default=False)
    gym_count           = models.IntegerField(default=0)
    gym_buffer_count    = models.IntegerField(default=0)
    salon_allowed      = models.BooleanField(default=False)
    salon_count        = models.IntegerField(default=0)
    salon_buffer_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'space_mapping_version'

class ProposalInfo(BaseModel):
    """
    Two extra fields called parent and is_campaign is added. parent is a self referencing field. it refers to itself.
    parent stores the information that from what proposal_id, the current proposal_id was created.
    is_campaign determines weather this proposal is a campaign or not.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    proposal_id = models.CharField(max_length=255, primary_key=True)
    account = models.ForeignKey('AccountInfo', related_name='proposals',on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.BooleanField(default=False,)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_by = models.CharField(max_length=50, default='Admin')
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.CharField(max_length=50, default='Admin')
    tentative_cost = models.IntegerField(default=5000)
    tentative_start_date = models.DateTimeField(null=True)
    tentative_end_date = models.DateTimeField(null=True)
    campaign_state = models.CharField(max_length=10, null=True, blank=True)
    parent = models.ForeignKey('ProposalInfo', null=True, blank=True, default=None)
    objects = managers.GeneralManager()
    invoice_number = models.CharField(max_length=1000, null=True, blank=True)

    def get_centers(self):
        try:
            return self.centers.all()
        except:
            return None
    def get_proposal_versions(self):
        return self.proposal_versions.all().order_by('-timestamp')

    class Meta:

        db_table = 'proposal_info'

class ProposalInfoVersion(models.Model):
    # proposal_id         = models.CharField(db_column = 'PROPOSAL ID',max_length=15,primary_key=True)
    # account             = models.ForeignKey(AccountInfo,related_name='proposals', db_column ='ACCOUNT',on_delete=models.CASCADE)
    proposal            = models.ForeignKey('ProposalInfo', related_name='proposal_versions', db_column='PROPOSAL', on_delete=models.CASCADE)
    name                = models.CharField(db_column='NAME', max_length=50,blank=True)
    payment_status      = models.BooleanField(default=False, db_column='PAYMENT STATUS')
    # updated_on          = models.DateTimeField(auto_now=True, auto_now_add=False)
    # updated_by          = models.CharField(max_length=50,default='Admin')
    created_on          = models.DateTimeField()
    created_by          = models.CharField(max_length=50, default='Admin')
    tentative_cost      = models.IntegerField(default=5000)
    tentative_start_date = models.DateTimeField(null=True)
    tentative_end_date  = models.DateTimeField(null=True)
    timestamp           = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        #db_table = 'PROPOSAL_INFO_VERSION'
        db_table = 'proposal_info_version'

class ProposalMasterCost(BaseModel):
    """
    A table to store revenue related costs. currently it's content will be populated by a sheet. only fixed fields
    and relations are covered up.
    Only one instance of MasterCost exists for one proposal version, proposal
    proposal_version alone does not make any sense. it's always tied to a proposal instance.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    proposal = models.OneToOneField('ProposalInfo', null=True, blank=True)
    agency_cost = models.FloatField(null=True, blank=True)
    basic_cost = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    total_cost = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    total_impressions = models.FloatField(null=True, blank=True)
    average_cost_per_impression = models.FloatField(null=True, blank=True)
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'proposal_master_cost_details'

class ProposalMetrics(BaseModel):
    """
    Different types of  spaces/suppliers will have different metrics. a metrics is list of predefined headers.
    one supplier can have many metrices. hence this model is used to store data for a given supplier that
    exists as a list of values.
    for proposal x, metric m1 has value of v1 for supplier S.
    for proposal x, metric m2 has value of v2 for supplier S.
    """
    proposal_master_cost = models.ForeignKey(ProposalMasterCost, null=True, blank=True)
    metric_name = models.CharField(max_length=255, null=True, blank=True)
    supplier_type = models.ForeignKey(ContentType, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'proposal_metrics'

class ProposalCenterSuppliers(BaseModel):
    """
    which suppliers are allowed in a given center under a proposal ?
    used when CreateInitialProposal is called. each center can have different suppliers allowed.
    each supplier is identified by a content_type and a unique code predefined for it.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    proposal = models.ForeignKey('ProposalInfo', null=True, blank=True)
    center = models.ForeignKey('ProposalCenterMapping', null=True, blank=True)
    supplier_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    supplier_type_code = models.CharField(max_length=255, null=True, blank=True)
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'proposal_center_suppliers'

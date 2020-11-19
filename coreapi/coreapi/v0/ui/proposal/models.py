from django.conf import settings
from django.db import models
from v0 import managers
from django.contrib.contenttypes.models import ContentType
from v0.ui.base.models import BaseModel
from v0.ui.finances.models import ProposalMasterCost
from v0.constants import supplier_id_max_length
from django.contrib.contenttypes import fields


class ProposalCenterMapping(BaseModel):
    """
    for a given proposal, stores lat, long, radius, city, pincode etc.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    proposal = models.ForeignKey('ProposalInfo', db_index=True, related_name='centers', on_delete=models.CASCADE)
    center_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150, null=True, blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    radius = models.FloatField(default=0.0)
    subarea = models.CharField(max_length=35)
    area = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    pincode = models.IntegerField()
    objects = managers.GeneralManager()

    def get_space_mappings(self):
        return SpaceMapping.objects.get(center=self)

    class Meta:
        db_table = 'proposal_center_mapping'
        unique_together = (('proposal', 'center_name'),)


class ProposalCenterMappingVersion(models.Model):
    proposal_version = models.ForeignKey("ProposalInfoVersion", db_index=True, related_name='centers_version',
                                         on_delete=models.CASCADE)
    center_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    subarea = models.CharField(max_length=35, default='')
    area = models.CharField(max_length=35, default='')
    city = models.CharField(max_length=35, default='')
    pincode = models.IntegerField(default=0)

    def get_space_mappings_versions(self):
        return SpaceMappingVersion.objects.get(center_version=self)

    class Meta:
        db_table = 'proposal_center_mapping_version'
        unique_together = (('proposal_version', 'center_name'),)


class SpaceMapping(models.Model):
    """
    This model talks about what spaces or suppliers are allowed or not at a center for a given proposal.
    """
    center = models.OneToOneField(ProposalCenterMapping, db_index=True, related_name='space_mappings',
                                  on_delete=models.CASCADE)
    proposal = models.ForeignKey('ProposalInfo', related_name='space_mapping', on_delete=models.CASCADE)
    society_allowed = models.BooleanField(default=False)
    society_count = models.IntegerField(default=0)
    society_buffer_count = models.IntegerField(default=0)
    corporate_allowed = models.BooleanField(default=False)
    corporate_count = models.IntegerField(default=0)
    corporate_buffer_count = models.IntegerField(default=0)
    gym_allowed = models.BooleanField(default=False)
    gym_count = models.IntegerField(default=0)
    gym_buffer_count = models.IntegerField(default=0)
    salon_allowed = models.BooleanField(default=False)
    salon_count = models.IntegerField(default=0)
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
        # db_table = 'SPACE_MAPPING'
        db_table = 'space_mapping'


class SpaceMappingVersion(models.Model):
    center_version = models.OneToOneField(ProposalCenterMappingVersion, db_index=True,
                                          related_name='space_mappings_version', on_delete=models.CASCADE)
    proposal_version = models.ForeignKey('ProposalInfoVersion', related_name='space_mapping_version',
                                         on_delete=models.CASCADE)
    society_allowed = models.BooleanField(default=False)
    society_count = models.IntegerField(default=0)
    society_buffer_count = models.IntegerField(default=0)
    corporate_allowed = models.BooleanField(default=False)
    corporate_count = models.IntegerField(default=0)
    corporate_buffer_count = models.IntegerField(default=0)
    gym_allowed = models.BooleanField(default=False)
    gym_count = models.IntegerField(default=0)
    gym_buffer_count = models.IntegerField(default=0)
    salon_allowed = models.BooleanField(default=False)
    salon_count = models.IntegerField(default=0)
    salon_buffer_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'space_mapping_version'


class ProposalInfo(BaseModel):
    """
    Two extra fields called parent and is_campaign is added. parent is a self referencing field. it refers to itself.
    parent stores the information that from what proposal_id, the current proposal_id was created.
    is_campaign determines weather this proposal is a campaign or not.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    proposal_id = models.CharField(db_index=True, max_length=255, primary_key=True)
    account = models.ForeignKey('AccountInfo', related_name='proposals', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.BooleanField(default=False, )
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_by = models.CharField(max_length=50, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    tentative_cost = models.IntegerField(default=5000)
    tentative_start_date = models.DateTimeField(null=True)
    tentative_end_date = models.DateTimeField(null=True)
    campaign_state = models.CharField(max_length=10, null=True, blank=True)
    parent = models.ForeignKey('ProposalInfo', null=True, blank=True, default=None, on_delete=models.CASCADE)
    objects = managers.GeneralManager()
    is_disabled = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=1000, null=True, blank=True)
    principal_vendor = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    brand = models.CharField(choices=(( 'single_brand', 'single_brand' ),  ('multi_brand', 'multi_brand')), max_length=60, blank=True, null=True)
    is_mix = models.BooleanField(default=False)
    type_of_end_customer = models.ForeignKey('TypeOfEndCustomer', null=True, on_delete=models.CASCADE)

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
    proposal = models.ForeignKey('ProposalInfo', related_name='proposal_versions', db_column='PROPOSAL',
                                 on_delete=models.CASCADE)
    name = models.CharField(db_column='NAME', max_length=50, blank=True)
    payment_status = models.BooleanField(default=False, db_column='PAYMENT STATUS')
    # updated_on          = models.DateTimeField(auto_now=True, auto_now_add=False)
    # updated_by          = models.CharField(max_length=50,default='Admin')
    created_on = models.DateTimeField()
    created_by = models.CharField(max_length=50, default='Admin')
    tentative_cost = models.IntegerField(default=5000)
    tentative_start_date = models.DateTimeField(null=True)
    tentative_end_date = models.DateTimeField(null=True)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        # db_table = 'PROPOSAL_INFO_VERSION'
        db_table = 'proposal_info_version'


class ProposalMetrics(BaseModel):
    """
    Different types of  spaces/suppliers will have different metrics. a metrics is list of predefined headers.
    one supplier can have many metrices. hence this model is used to store data for a given supplier that
    exists as a list of values.
    for proposal x, metric m1 has value of v1 for supplier S.
    for proposal x, metric m2 has value of v2 for supplier S.
    """
    proposal_master_cost = models.ForeignKey(ProposalMasterCost, null=True, blank=True, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=255, null=True, blank=True)
    supplier_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    value = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'proposal_metrics'


class ProposalCenterSuppliers(BaseModel):
    """
    which suppliers are allowed in a given center under a proposal ?
    used when CreateInitialProposal is called. each center can have different suppliers allowed.
    each supplier is identified by a content_type and a unique code predefined for it.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    proposal = models.ForeignKey('ProposalInfo', null=True, blank=True, on_delete=models.CASCADE)
    center = models.ForeignKey('ProposalCenterMapping', null=True, blank=True, on_delete=models.CASCADE)
    supplier_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    supplier_type_code = models.CharField(max_length=255, null=True, blank=True)
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'proposal_center_suppliers'


class ImageMapping(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    location_id = models.CharField(db_column='LOCATION_ID', max_length=20, blank=True, null=True)
    location_type = models.CharField(db_column='LOCATION_TYPE', max_length=20, blank=True, null=True)
    supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='images', blank=True,
                                 null=True, on_delete=models.CASCADE)
    image_url = models.CharField(db_column='IMAGE_URL', max_length=100)
    comments = models.TextField(db_column='COMMENTS', blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'image_mapping'


class ShortlistedSpacesVersion(models.Model):
    space_mapping_version = models.ForeignKey('SpaceMappingVersion', db_index=True, related_name='spaces_version',
                                              on_delete=models.CASCADE)
    supplier_code = models.CharField(max_length=4)
    content_type = models.ForeignKey(ContentType, related_name='spaces_version', on_delete=models.CASCADE)
    object_id = models.CharField(max_length=12)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    buffer_status = models.BooleanField(default=False)

    class Meta:
        # db_table = 'SHORTLISTED_SPACES_VERSION'
        db_table = 'shortlisted_spaces_version'


class ShortlistedSpaces(BaseModel):
    """
    This model stores all the shortlisted spaces. One Supplier or space can be under different campaigns.
    in one campaign it's status can be removed while in the other it's buffered. Hence this model is made
    for mapping such relations.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    space_mapping = models.ForeignKey('SpaceMapping', db_index=True, related_name='spaces', on_delete=models.CASCADE,
                                      null=True, blank=True)
    center = models.ForeignKey('ProposalCenterMapping', null=True, blank=True, on_delete=models.CASCADE)
    proposal = models.ForeignKey('ProposalInfo', null=True, blank=True, on_delete=models.CASCADE)
    supplier_code = models.CharField(max_length=4, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, related_name='spaces', on_delete=models.CASCADE)
    object_id = models.CharField(db_index=True, max_length=supplier_id_max_length)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    buffer_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, null=True, blank=True)
    objects = managers.GeneralManager()
    campaign_status = models.CharField(max_length=10, default='', null=True, blank=True)
    phase = models.CharField(max_length=10, default='', null=True, blank=True)
    payment_status = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    beneficiary_name = models.CharField(max_length=255, null=True, blank=True)
    ifsc_code = models.CharField(max_length=30, blank=True, null=True)
    account_number = models.CharField(max_length=250, blank=True, null=True)
    payment_message = models.CharField(max_length=255, null=True, blank=True)
    total_negotiated_price = models.CharField(max_length=255, null=True, blank=True)
    booking_status = models.CharField(max_length=10, default='NI')
    booking_sub_status = models.CharField(max_length=15, null=True, blank=True)
    bk_status = models.ForeignKey('BookingStatus', null=True, on_delete=models.CASCADE)
    bk_substatus = models.ForeignKey('BookingSubstatus', null=True, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    transaction_or_check_number = models.CharField(max_length=50, null=True, blank=True)
    phase_no = models.ForeignKey('SupplierPhase', blank=True, null=True, on_delete=models.PROTECT)
    freebies = models.CharField(max_length=255, null=True, blank=True)
    stall_locations = models.CharField(max_length=255, null=True, blank=True)
    cost_per_flat = models.FloatField(null=True, blank=True)
    booking_priority = models.CharField(max_length=10,null=True,blank=True)
    sunboard_location = models.CharField(max_length=50,null=True,blank=True)
    next_action_date = models.DateTimeField(null=True)
    last_call_date = models.DateTimeField(null=True)
    brand_organisation_id = models.CharField(max_length=255, null=True, blank=True)
    permission_box_image = models.CharField(max_length=255, null=True, blank=True)
    receipt_image = models.CharField(max_length=255, null=True, blank=True)
    assigned_user = models.CharField(max_length=255, null=True, blank=True)
    assigned_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    requirement_given = models.CharField(max_length=5, default="no")
    requirement_given_date = models.DateTimeField(null=True)
    color_code = models.IntegerField(null=True, default=4)

    class Meta:
        db_table = 'shortlisted_spaces'


class HashTagImages(BaseModel):
    """
    This model stores campaign images which is hashtagged by BANNER,RECEIPT...etc
    """
    campaign = models.ForeignKey('ProposalInfo', null=False, blank=False, on_delete=models.CASCADE)
    object_id = models.CharField(db_index=True, max_length=100)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=1000, null=True, blank=True)
    hashtag = models.CharField(max_length=255)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'hashtag_images'


class SupplierPhase(BaseModel):
    """
    This model stores phase no of supplier and start date and end date
    """
    phase_no = models.CharField(max_length=10, default='', null=True, blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    comments = models.CharField(max_length=255, null=True, blank=True)
    campaign = models.ForeignKey('ProposalInfo', null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'supplier_phase'

class SupplierAssignment(BaseModel):
    """
    This model stores supplier assignment
    """
    campaign = models.ForeignKey('ProposalInfo', null=False, blank=False, on_delete=models.CASCADE)
    supplier_id = models.CharField(db_index=True, max_length=supplier_id_max_length)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey('BaseUser', related_name="assigned_by_user", null=False, blank=False, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey('BaseUser', related_name="assigned_to_user", null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'supplier_assignment'

class TypeOfEndCustomer(BaseModel):
    name = models.CharField(max_length=255)
    formatted_name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'type_of_end_customer'

class BookingStatus(BaseModel):
    type_of_end_customer = models.ForeignKey('TypeOfEndCustomer', null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    class Meta:
        db_table = 'booking_status'

class BookingSubstatus(BaseModel):
    booking_status = models.ForeignKey('BookingStatus', null=False, blank=False, on_delete=models.CASCADE, related_name ='booking_substatus')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    class Meta:
        db_table = 'booking_substatus'
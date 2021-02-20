from django.db import models
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from django.conf import settings

IMPL_TIMELINE_CATEGORY = (
    ('within next 2 days', 'within next 2 days'),
    ('2 days to 1 week', '2 days to 1 week'),
    ('1 week to 2 weeks', '1 week to 2 weeks'),
    ('less than 1 month', 'less than 1 month'),
    ('within 2 weeks', 'within 2 weeks'),
    ('2 weeks to 1 month', '2 weeks to 1 month'),
    ('within 1 month','within 1 month'),
    ('within 2 months','within 2 months'),
    ('1 month to 2 months', '1 month to 2 months'),
    ('2 months to 4 months', '2 months to 4 months'),
    ('4 months to 6 months', '4 months to 6 months'),
    ('after 6 months', 'after 6 months'),
    ('1 month to 3 months', '1 month to 3 months'),
    ('2 months to 6 months', '2 months to 6 months'),
    ('3 months to 6 months', '3 months to 6 months'),
    ('6 months to 9 months', '6 months to 9 months'),
    ('9 months to 1 year', '9 months to 1 year'),
    ('6 months to 1 year', '6 months to 1 year'),
    ('1 year to 1.5 years', '1 year to 1.5 years'),
    ('not yet decided', 'not yet decided'),
    ('not given', 'not given')
)

MEATING_TIMELINE_CATEGORY = (
    ('as soon as possible', 'as soon as possible'),
    ('within 1 week', 'within 1 week'),
    ('within a fortnight (2 weeks)', 'within a fortnight (2 weeks)'),
    ('within a month', 'within a month'),
    ('not given', 'not given')
)

LEAD_STATUS_CATEGORY = (
    ('Very Deep Lead', 'Very Deep Lead'),
    ('Deep Lead', 'Deep Lead'),
    ('Hot Lead', 'Hot Lead'),
    ("Lead", "Lead"),
    ("Raw Lead", "Raw Lead"),
    ('Warm Lead', 'Warm Lead')
)

CURRENT_PATNER_FEEDBACK = (
    ('NA','NA'),
    ('Satisfied', 'Satisfied'),
    ('Dissatisfied', 'Dissatisfied'),
    ('Extremely Dissatisfied', 'Extremely Dissatisfied'),
)

CALL_BACK_PREFERENCE = (
    ('NA','NA'),
    ('anytime', 'anytime'),
    ('no need of call. arrange a meeting directly', 'no need of call. arrange a meeting directly'),
    ('weekday morning', 'weekday morning'),
    ("weekday evening", "weekday evening"),
    ("weekend morning", "weekend morning"),
    ('weekend evening', 'weekend evening'),
    ("customized calling period", "customized calling period"),
)

GLOBAL_HOT_LEAD_VALUE = (
    ('H1','H1'),
    ('H2','H2'),
    ('H3','H3'),
    ('H4','H4'),
    ('H5','H5'),
    ('H6','H6'),
)

CLIENT_STATUS = (
    ('Accepted','Accepted'),
    ('Decision Pending','Decision Pending'),
    ('Decline','Decline'),
)


class Requirement(models.Model):
    campaign = models.ForeignKey('ProposalInfo', null=True, blank=True, on_delete=models.CASCADE)
    shortlisted_spaces = models.ForeignKey('ShortlistedSpaces', null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='company')
    current_company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='current')
    current_company_other =  models.CharField(max_length=50, null=True, blank=True)
    preferred_company = models.ManyToManyField('Organisation', null=True, blank=True, related_name='preferred')
    preferred_company_other =  models.CharField(max_length=50, null=True, blank=True)
    sector = models.ForeignKey('BusinessTypes', null=True, blank=True, on_delete=models.CASCADE)
    sub_sector = models.ForeignKey('BusinessSubTypes', null=True, blank=True, on_delete=models.CASCADE)
    lead_by = models.ForeignKey('ContactDetails', null=True, blank=True, on_delete=models.CASCADE)
    impl_timeline = models.CharField(max_length=30, choices=IMPL_TIMELINE_CATEGORY, default=IMPL_TIMELINE_CATEGORY[1][0]) # implementation_timeline
    meating_timeline = models.CharField(max_length=30, choices=MEATING_TIMELINE_CATEGORY, default=MEATING_TIMELINE_CATEGORY[1][0]) # meating_timeline
    lead_status = models.CharField(max_length=30, choices=LEAD_STATUS_CATEGORY, default=LEAD_STATUS_CATEGORY[1][0])
    comment = models.TextField(max_length=500, null=True, blank=True)
    is_current_patner = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    current_patner_feedback = models.CharField(max_length=50, choices=CURRENT_PATNER_FEEDBACK, default="NA")
    current_patner_feedback_reason = models.CharField(max_length=250, null=True, blank=True)
    varified_ops = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    varified_ops_date = models.DateTimeField(null=True)
    varified_bd = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    varified_bd_date = models.DateTimeField(null=True)
    varified_bd_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    is_deleted = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    lead_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    l1_answers = models.CharField(max_length=100, null=True, blank=True)
    l1_answer_2 = models.CharField(max_length=100, null=True, blank=True)
    l2_answers = models.CharField(max_length=100, null=True, blank=True)
    l2_answer_2 = models.CharField(max_length=100, null=True, blank=True)
    varified_ops_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='varified_ops_by')
    company_campaign = models.ForeignKey('ProposalInfo', null=True, blank=True, on_delete=models.CASCADE, related_name='company_campaign')
    company_shortlisted_spaces = models.ForeignKey('ShortlistedSpaces', null=True, blank=True, on_delete=models.CASCADE, related_name='company_shortlisted_spaces')
    change_current_patner = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    lead_price = models.FloatField(default=0.0, blank=True, null=True)
    call_back_preference = models.CharField(max_length=100, choices=CALL_BACK_PREFERENCE, default="NA")
    lead_purchased = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="yes")
    purchased_date = models.DateTimeField(null=True)
    is_preferred_company = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    hotness_of_lead = models.CharField(max_length=5, choices=GLOBAL_HOT_LEAD_VALUE, default="H1")
    client_status = models.CharField(max_length=20, choices=CLIENT_STATUS, default="Decision Pending")

    class Meta:
        db_table = 'requirement'

class PreRequirement(models.Model):
    campaign = models.ForeignKey('ProposalInfo', null=True, blank=True, on_delete=models.CASCADE, related_name='campaign')
    shortlisted_spaces = models.ForeignKey('ShortlistedSpaces', null=True, blank=True, on_delete=models.CASCADE, related_name='shortlisted')
    company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='pre_company')
    current_company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='pre_current')
    current_company_other =  models.CharField(max_length=50, null=True, blank=True)
    preferred_company = models.ManyToManyField('Organisation', null=True, blank=True, related_name='pre_preferred')
    preferred_company_other =  models.CharField(max_length=50, null=True, blank=True)
    sector = models.ForeignKey('BusinessTypes', null=True, blank=True, on_delete=models.CASCADE, related_name='sector')
    sub_sector = models.ForeignKey('BusinessSubTypes', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_Sector')
    lead_by = models.ForeignKey('ContactDetails', null=True, blank=True, on_delete=models.CASCADE, related_name='contact')
    impl_timeline = models.CharField(max_length=30, choices=IMPL_TIMELINE_CATEGORY, default=IMPL_TIMELINE_CATEGORY[1][0]) # implementation_timeline
    meating_timeline = models.CharField(max_length=30, choices=MEATING_TIMELINE_CATEGORY, default=MEATING_TIMELINE_CATEGORY[1][0]) # meating_timeline
    lead_status = models.CharField(max_length=30, choices=LEAD_STATUS_CATEGORY, default=LEAD_STATUS_CATEGORY[1][0])
    comment = models.TextField(max_length=500, null=True, blank=True)
    is_current_patner = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    current_patner_feedback = models.CharField(max_length=50, choices=CURRENT_PATNER_FEEDBACK, default="NA")
    current_patner_feedback_reason = models.CharField(max_length=250, null=True, blank=True)
    varified_ops = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    varified_ops_date = models.DateTimeField(null=True)
    varified_bd = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    varified_bd_date = models.DateTimeField(null=True)
    varified_bd_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='pre_varified_bd_by')
    is_deleted = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    lead_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    l1_answers = models.CharField(max_length=100, null=True, blank=True)
    l1_answer_2 = models.CharField(max_length=100, null=True, blank=True)
    l2_answers = models.CharField(max_length=100, null=True, blank=True)
    l2_answer_2 = models.CharField(max_length=100, null=True, blank=True)
    varified_ops_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='pre_varified_ops_by')
    company_campaign = models.ForeignKey('ProposalInfo', null=True, blank=True, on_delete=models.CASCADE, related_name='pre_company_campaign')
    company_shortlisted_spaces = models.ForeignKey('ShortlistedSpaces', null=True, blank=True, on_delete=models.CASCADE, related_name='pre_company_shortlisted_spaces')
    change_current_patner = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    lead_price = models.FloatField(default=0.0, blank=True, null=True)
    call_back_preference = models.CharField(max_length=100, choices=CALL_BACK_PREFERENCE, default="NA")
    lead_purchased = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="yes")
    purchased_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'pre_requirement'

class SuspenseLead(MongoModel):
    phone_number = fields.CharField(blank=True)
    supplier_name = fields.CharField(blank=True)
    pin_code = fields.CharField(blank=True)
    poc_name = fields.CharField(blank=True)
    designation = fields.CharField(blank=True)
    supplier_type = fields.CharField(blank=True)
    city = fields.CharField(blank=True)
    area = fields.CharField(blank=True)
    sub_area = fields.CharField(blank=True)
    sector_name = fields.CharField(blank=True)
    sub_sector_name = fields.CharField(blank=True)
    implementation_timeline = fields.CharField(blank=True)
    meating_timeline = fields.CharField(blank=True)
    lead_status = fields.CharField(blank=True)
    comment = fields.CharField(blank=True)
    current_patner = fields.CharField(blank=True)
    current_patner_feedback = fields.CharField(blank=True)
    current_patner_feedback_reason = fields.CharField(blank=True)
    prefered_patners = fields.ListField(blank=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    l1_answers = fields.CharField(blank=True)
    l1_answer_2 = fields.CharField(blank=True)
    l2_answers = fields.CharField(blank=True)
    l2_answer_2 = fields.CharField(blank=True)
    call_back_preference = fields.CharField(blank=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'

class BrowsedLead(MongoModel):
    supplier_id = fields.CharField(blank=True)
    shortlisted_spaces_id = fields.CharField(blank=True)
    campaign_id = fields.CharField(blank=True)
    phone_number = fields.CharField(blank=True)
    supplier_name = fields.CharField(blank=True)
    city = fields.CharField(blank=True)
    area = fields.CharField(blank=True)
    sub_area = fields.CharField(blank=True)
    sector_id = fields.CharField(blank=True)
    sub_sector_id = fields.CharField(blank=True)
    implementation_timeline = fields.CharField(blank=True)
    meating_timeline = fields.CharField(blank=True)
    lead_status = fields.CharField(blank=True)
    comment = fields.CharField(blank=True)
    current_patner_id = fields.CharField(blank=True)
    current_patner_other = fields.CharField(blank=True)
    prefered_patners = fields.ListField(blank=True)
    prefered_patner_other = fields.CharField(blank=True)
    current_patner_feedback = fields.CharField(blank=True)
    current_patner_feedback_reason = fields.CharField(blank=True)
    status = fields.ListField(blank=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    l1_answers = fields.CharField(blank=True)
    l1_answer_2 = fields.CharField(blank=True)
    l2_answers = fields.CharField(blank=True)
    l2_answer_2 = fields.CharField(blank=True)
    call_back_preference = fields.CharField(blank=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class CampaignLeads(MongoModel):
    purchased_count = fields.CharField(blank=True)
    lead_count = fields.CharField(blank=True)
    company_campaign_id = fields.CharField(blank=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'

class OrganizationLeads(MongoModel):
    purchased_count = fields.CharField(blank=True)
    lead_count = fields.CharField(blank=True)
    company_id = fields.CharField(blank=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class SalesRepresentatives(models.Model):
    company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='sales_org')
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NotificationTemplates(models.Model):
    content = models.TextField(max_length=500, null=True, blank=True)
    notification_type = models.CharField(max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MachadaloRelationshipManager(models.Model):
    company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='relation_org')
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PaymentDetails(models.Model):
    company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='payment_org')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=30, null=True, blank=True)
    url = models.CharField(max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_details'

class LicenseDetails(models.Model):
    company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='license_org')
    website_url = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)
    gstin_number = models.CharField(max_length=80, null=True, blank=True)
    registered_address = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    pin_code = models.CharField(max_length=50, null=True, blank=True)
    billing_address = models.CharField(max_length=500, null=True, blank=True)
    pan_number = models.CharField(max_length=50, null=True, blank=True)
    poc_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'license_details'




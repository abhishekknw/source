from django.db import models

IMPL_TIMELINE_CATEGORY = (
    ('immediate', 'immediate'),
    ('next 2-4 months', 'next 2-4 months'),
    ('after 4 months', 'after 4 months'),
    ("don't know", "don't know")
)

MEATING_TIMELINE_CATEGORY = (
    ('immediate', 'immediate'),
    ('next 15 days-2 months', 'next 15 days-2 months'),
    ('after 2 months', 'after 2 months'),
    ("don't know", "don't know")
)

LEAD_STATUS_CATEGORY = (
    ('very_deep_lead', 'very_deep_lead'),
    ('deep_lead', 'deep_lead'),
    ('hot_lead', 'hot_lead'),
    ("lead", "lead"),
    ("raw_lead", "raw_lead")
)

class Requirement(models.Model):
    campaign = models.ForeignKey('ProposalInfo', null=True, blank=True, on_delete=models.CASCADE)
    shortlisted_spaces = models.ForeignKey('ShortlistedSpaces', null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='company')
    current_company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='current')
    preferred_company = models.ManyToManyField('Organisation', null=True, blank=True, related_name='preferred')
    sector = models.ForeignKey('BusinessTypes', null=True, blank=True, on_delete=models.CASCADE)
    sub_sector = models.ForeignKey('BusinessSubTypes', null=True, blank=True, on_delete=models.CASCADE)
    lead_by = models.ForeignKey('ContactDetails', null=True, blank=True, on_delete=models.CASCADE)
    impl_timeline = models.CharField(max_length=30, choices=IMPL_TIMELINE_CATEGORY, default=IMPL_TIMELINE_CATEGORY[1][0]) # implementation_timeline
    meating_timeline = models.CharField(max_length=30, choices=MEATING_TIMELINE_CATEGORY, default=MEATING_TIMELINE_CATEGORY[1][0]) # meating_timeline
    lead_status = models.CharField(max_length=30, choices=LEAD_STATUS_CATEGORY, default=LEAD_STATUS_CATEGORY[1][0])
    comment = models.TextField(max_length=500, blank=True)
    varified = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'requirement'
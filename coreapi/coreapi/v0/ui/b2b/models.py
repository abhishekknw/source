from django.db import models

class Sector(models.Model):
    name = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'sector'

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
    shortlisted_spaces = models.ForeignKey('ShortlistedSpaces', null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='preferred')
    current_company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='current')
    sector = models.ForeignKey('Sector', null=True, blank=True, on_delete=models.CASCADE)
    impl_timeline = models.CharField(max_length=30, choices=IMPL_TIMELINE_CATEGORY, default=IMPL_TIMELINE_CATEGORY[1][0]) # implementation_timeline
    meating_timeline = models.CharField(max_length=30, choices=MEATING_TIMELINE_CATEGORY, default=MEATING_TIMELINE_CATEGORY[1][0]) # meating_timeline
    lead_status = models.CharField(max_length=30, choices=LEAD_STATUS_CATEGORY, default=LEAD_STATUS_CATEGORY[1][0])
    comment = models.TextField(max_length=500, blank=True)
    varified = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'requirement'
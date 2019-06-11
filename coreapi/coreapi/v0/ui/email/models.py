from django.db import models
from v0.ui.base.models import BaseModel
from django.conf import settings

EMAIL_TYPES = (
    ('WEEKLY_LEADS', 'WEEKLY_LEADS'),
    ('WEEKLY_LEADS_GRAPH', 'WEEKLY_LEADS_GRAPH'),
    ('BOOKING_DETAILS_BASIC', 'BOOKING_DETAILS_BASIC'),
    ('BOOKING_DETAILS_ADV', 'BOOKING_DETAILS_ADV')
)

USER_TYPES = (
    ('NORMAL', 'NORMAL'),
    ('ADMIN', 'ADMIN'),
)


class EmailSettings(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)
    email_type = models.CharField(max_length=70, null=True, choices=EMAIL_TYPES)
    is_allowed = models.BooleanField(default=False)
    last_sent = models.DateTimeField(null=True)
    user_type = models.CharField(max_length=70, null=True, choices=USER_TYPES, default="NORMAL")
    class Meta:
        db_table = 'email_settings'
        unique_together = ('user', 'email_type',)
import datetime
from django.core.management.base import BaseCommand, CommandError
from v0.ui.society_resident_details.utils import get_last_24_hour_leads


class Command(BaseCommand):
    help = 'Daily lead to user conversion'

    def handle(self, *args, **options):
        get_last_24_hour_leads()
        return
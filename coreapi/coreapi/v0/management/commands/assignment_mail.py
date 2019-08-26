import datetime
from django.core.management.base import BaseCommand, CommandError
from v0.ui.proposal.models import SupplierPhase
from v0.ui.email.tasks import send_booking_mails_ctrl


class Command(BaseCommand):
    help = 'Daily assignment mail'

    def handle(self, *args, **options):
        current_date = datetime.datetime.now().date()
        phases = SupplierPhase.objects.filter(start_date__lte=current_date, end_date__gte=current_date).all()
        for phase in phases:
            campaign_id = phase.campaign_id
            send_booking_mails_ctrl('daily_assignment_mail.html', campaign_id)
        return
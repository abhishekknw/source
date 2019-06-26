from __future__ import print_function
from __future__ import absolute_import
from django.core.management.base import BaseCommand, CommandError
from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces
from v0.ui.account.models import ContactDetails
from django.db.models import Q, F
import gpxpy.geo
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from celery import shared_task
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from django.db import connection
import csv
from v0.ui.email.views import send_mail_with_attachment
import datetime
from datetime import timedelta

class Command(BaseCommand):
	help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):

		end_date = datetime.datetime.now().date()
		start_date = end_date - datetime.timedelta(days=700)

		if start_date:
			all_campaigns = ProposalInfo.objects.filter(tentative_start_date__gte=start_date).all()
		else:
			all_campaigns = ProposalInfo.objects.all()
		return_list = []
		for campaign in all_campaigns:
			try:
				if "BYJU" in campaign.name:
					partial_dict = {"campaign name": campaign.name,
									"total supplier count": None,
					                "total contacts with name": 0, 
					                "total contacts with number": 0,
					                }
					all_shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign.proposal_id).all()
					all_supplier_ids = [ss.object_id for ss in all_shortlisted_spaces]
					all_suppliers = ContactDetails.objects.filter(object_id__in=all_supplier_ids)
					partial_dict["total supplier count"] = len(all_shortlisted_spaces)
					for sc in all_suppliers:
						if sc.mobile:
							partial_dict["total contacts with number"] += 1
						if sc.name:
							partial_dict["total contacts with name"] += 1
					return_list.append(partial_dict)
			except TypeError:
				pass
		writeExcel(return_list)

def writeExcel(return_list):

    toCSV = return_list
    try:
        keys = toCSV[0].keys()
    except IndexError:
        keys = 'null'
    with open('mis_contacts_reports.xls', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)
    subject = "Daily MIS contacts report"
    to = ("shailesh.singh@machadalo.com", "abaadada@machadalo.com")

    send_mail_with_attachment("mis_contacts_reports.xls", subject, to)
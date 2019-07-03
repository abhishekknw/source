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
from v0.ui.email.views import send_mail_with_attachment, send_mail_generic
import datetime
from datetime import timedelta
from django.template.loader import get_template


class Command(BaseCommand):
	help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):

		end_date = datetime.datetime.now().date()
		start_date = end_date - datetime.timedelta(days=10000)

		all_campaigns = ProposalInfo.objects.filter(tentative_start_date__gte=start_date).all()
		return_list = []
		for campaign in all_campaigns:
			try:
				if "BYJ" in campaign.proposal_id:
					partial_dict = {"campaign_name": campaign.name,
					                "total_supplier_count": None,
					                "total_contacts_with_name": 0, 
					                "total_contacts_with_number": 0,
					                }
					all_shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign.proposal_id).all()
					all_supplier_ids = [ss.object_id for ss in all_shortlisted_spaces]
					all_suppliers = ContactDetails.objects.filter(object_id__in=all_supplier_ids)
					partial_dict["total_supplier_count"] = len(all_shortlisted_spaces)
					for sc in all_suppliers:
					    if sc.mobile:
					        partial_dict["total_contacts_with_number"] += 1
					    if sc.name:
					        partial_dict["total_contacts_with_name"] += 1


					cursor = connection.cursor()
					cursor.execute("SELECT DISTINCT e.society_name, d.proposal_id, r.hashtag, e.Society_City, e.SOCIETY_LOCALITY \
					from shortlisted_inventory_pricing_details as c \
					inner join inventory_activity_assignment as a \
					inner join inventory_activity as b \
					inner join shortlisted_spaces as d \
					inner join supplier_society as e \
					inner join hashtag_images as r \
					on b.id = a.inventory_activity_id and b.shortlisted_inventory_details_id = c.id \
					and c.shortlisted_spaces_id = d.id and d.object_id = e.SUPPLIER_ID and r.object_id = e.supplier_id \
					where d.proposal_id in (%s) and a.activity_date between %s and %s and r.hashtag \
					= 'PERMISSION BOX'", [campaign.proposal_id,start_date, end_date])
					all_list_pb = cursor.fetchall()

					dict_details=['society_name', 'campaign_id', 'hashtag', 'society_city', 'society_locality']
					all_details_list_pb=[dict(zip(dict_details,l)) for l in all_list_pb]

					cursor.execute("SELECT DISTINCT e.society_name, d.proposal_id, r.hashtag, e.Society_City, e.SOCIETY_LOCALITY \
					from shortlisted_inventory_pricing_details as c \
					inner join inventory_activity_assignment as a \
					inner join inventory_activity as b \
					inner join shortlisted_spaces as d \
					inner join supplier_society as e \
					inner join hashtag_images as r \
					on b.id = a.inventory_activity_id and b.shortlisted_inventory_details_id = c.id \
					and c.shortlisted_spaces_id = d.id and d.object_id = e.SUPPLIER_ID and r.object_id = e.supplier_id \
					where d.proposal_id in (%s) and a.activity_date between %s and %s and r.hashtag \
					= 'RECEIPT'", [campaign.proposal_id,start_date, end_date])
					all_list_receipt = cursor.fetchall()
					all_shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign.proposal_id, is_completed=True).all()
					all_supplier_ids = [ss.object_id for ss in all_shortlisted_spaces]
					dict_details=['society_name', 'campaign_id', 'hashtag', 'society_city', 'society_locality']
					all_details_list_receipt=[dict(zip(dict_details,l)) for l in all_list_receipt]
					partial_dict['count_permission'] = len(all_details_list_pb)
					partial_dict['count_receipt'] = len(all_details_list_receipt)
					partial_dict['supplier_count'] =  len(all_supplier_ids)

					return_list.append(partial_dict)

			except TypeError:
				pass
		writeExcel(return_list)
		template_name = "mis_report_contact.html"
		booking_template = get_template(template_name)

		html = booking_template.render(
		    {"partial_dict": return_list})

		subject = "MIS Report of CAMPAIGNS"
		to_array = ["shailesh.singh@machadalo.com", "sathya.sharma@machadalo.com", "divya.moses@machadalo.com", 
		            "shyamlee.khanna@machadalo.com","srishti.dhamija@machadalo.com", "nikita.walicha@machadalo.com", 
		            "prashantgupta888@gmail.com", "kwasi0883@gmail.com", "madhu.atri@machadalo.com", 
		            "tejas.pawar@machadalo.com", "jaya.murugan@machadalo.com", "muvaz.khan@machadalo.com",
		            "lokesh.kumar@machadalo.com", "vyoma.desai@machadalo.com", "lokesh.kumar@machadalo.com",
		            "anupam@machadalo.com", "Anmol.prabhu@machadalo.com", "abhishek.chandel@machadalo.com",
		            "momi.borah@machadalo.com"
		            ]
		# to_array=['shailesh.singh@machadalo.com']
		send_mail_generic(subject, to_array, html, None,None)

def writeExcel(return_list):

    toCSV = return_list
    try:
        keys = toCSV[0].keys()
    except IndexError:
        keys = 'null'
    with open('mis_report.xls', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)
    subject = "MIS Report of CAMPAIGNS"
    to =("shailesh.singh@machadalo.com", "sathya.sharma@machadalo.com", "divya.moses@machadalo.com", 
		            "shyamlee.khanna@machadalo.com","srishti.dhamija@machadalo.com", "nikita.walicha@machadalo.com", 
		            "prashantgupta888@gmail.com", "kwasi0883@gmail.com", "madhu.atri@machadalo.com", 
		            "tejas.pawar@machadalo.com", "jaya.murugan@machadalo.com", "muvaz.khan@machadalo.com",
		            "lokesh.kumar@machadalo.com", "vyoma.desai@machadalo.com", "lokesh.kumar@machadalo.com",
		            "anupam@machadalo.com", "Anmol.prabhu@machadalo.com", "abhishek.chandel@machadalo.com",
		            "momi.borah@machadalo.com")
    # to = ("shailesh.singh@machadalo.com", "abaadada@machadalo.com")

    send_mail_with_attachment("mis_report.xls", subject, to)
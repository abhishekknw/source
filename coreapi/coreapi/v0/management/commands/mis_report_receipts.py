from __future__ import print_function
from __future__ import absolute_import
from django.core.management.base import BaseCommand, CommandError
from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces
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

@shared_task()
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        end_date = datetime.datetime.now().date()
        start_date = end_date - datetime.timedelta(days=7)

        if start_date:
            all_campaigns = ProposalInfo.objects.all()
        else:
            all_campaigns = ProposalInfo.objects.all()
        return_list = []
        for campaign in all_campaigns:
            try:
                if "BYJU" in campaign.name:
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
                    return_list.append({"campaign name": campaign.name,
                                        "count permission": len(all_details_list_pb),
                                        "count receipt": len(all_details_list_receipt),
                                        "supplier count": len(all_supplier_ids)})
            except TypeError:
                pass

        writeExcel(return_list)


def writeExcel(return_list):

    toCSV = return_list
    try:
        keys = toCSV[0].keys()
    except IndexError:
        keys = 'null'
    with open('mis_reciept_reports.xls', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)
    subject = "Daily MIS receipt report"
    to = ("shailesh.singh@machadalo.com", "verma@machadalo.com")

    send_mail_with_attachment("mis_reciept_reports.xls", subject, to)
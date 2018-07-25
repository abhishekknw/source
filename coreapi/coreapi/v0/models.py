# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.

# codes for supplier Types  Society -> RS   Corporate -> CP  Gym -> GY   salon -> SA

from __future__ import unicode_literals

import managers
from django.conf import settings
# from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from v0.constants import supplier_id_max_length
from v0.ui.user.models import BaseUser
from v0.ui.base.models import BaseModel
from v0.ui.campaign.models import CampaignAssignment
from v0.ui.organisation.models import Organisation
from v0.ui.proposal.models import SpaceMapping, SpaceMappingVersion
from v0.ui.supplier.models import SupplierTypeCorporate

# class ShortlistedInventoryDetails(BaseModel):
#     """
#     This table stores information about Release Date, Audit Date, and Campaign Dates associated with each inventory_id
#     under each campaign. All inventories within this table are booked.Campaign is nothing but Proposal_id with is_campaign = True
#     """
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
#     inventory_content_type = models.ForeignKey(ContentType, null=True, blank=True)
#     inventory_id = models.CharField(max_length=255, null=True, blank=True)
#     campaign_id = models.ForeignKey(ProposalInfo, null=True, blank=True)
#     release_date = models.DateTimeField(default=timezone.now())
#     closure_date = models.DateTimeField(default=timezone.now())
#     factor = models.IntegerField(default=0.0, null=True)
#     center = models.ForeignKey('ProposalCenterMapping')
#     ad_inventory_type = models.ForeignKey('AdInventoryType', null=True)
#     ad_inventory_duration = models.ForeignKey('DurationType', null=True)
#     inventory_price = models.FloatField(default=0.0, null=True)
#     shortlisted_spaces = models.ForeignKey(ShortlistedSpaces, null=True, blank=True)
#     objects = managers.GeneralManager()
#

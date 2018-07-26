from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

import v0.models as models
from v0.ui.proposal.models import SpaceMapping, SpaceMappingVersion
from v0.ui.user.models import BaseUser
from v0.ui.finances.models import AuditDate, ShortlistedInventoryPricingDetails, PriceMappingDefault
from v0.ui.base.serializers import DurationTypeSerializer
from v0.ui.serializers import UISocietySerializer
from v0.ui.user.serializers import BaseUserSerializer
from v0.ui.account.models import AccountInfo, Profile, GenericExportFileName, BusinessTypes, BusinessSubTypes
from v0.ui.account.serializers import BusinessAccountContactSerializer
from v0.ui.campaign.models import Campaign, CampaignSocietyMapping, CampaignAssignment
from v0.ui.campaign.serializers import CampaignTypeMappingSerializer
from v0.ui.organisation.models import Organisation
from v0.ui.inventory.models import SocietyInventoryBooking, SupplierTypeSociety, InventoryActivityImage, \
    InventoryActivityAssignment, InventoryTypeVersion, InventoryType, InventoryActivity
from v0.ui.inventory.serializers import AdInventoryTypeSerializer
from v0.ui.proposal.models import ProposalCenterMapping, ProposalCenterMappingVersion, ShortlistedSpaces, \
    ShortlistedSpacesVersion
from v0.ui.proposal.serializers import ProposalInfoSerializer

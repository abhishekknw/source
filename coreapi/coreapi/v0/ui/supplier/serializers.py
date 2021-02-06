from __future__ import absolute_import
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import (AddressMaster, SupplierMaster, SupplierHording, SupplierEducationalInstitute, SupplierTypeSociety, SupplierTypeCode, SupplierTypeRetailShop, SupplierTypeBusShelter,
                    SupplierTypeGym, SupplierTypeSalon, SupplierTypeCorporate, SupplierInfo, CorporateBuilding,
                    CorporateParkCompanyList, CorporateCompanyDetails, SupplierTypeBusDepot, SupplierAmenitiesMap,
                    SupplierBus, SupplierGantry, SupplierRadioChannel, SupplierTvChannel, SupplierTypeHospital, SupplierCorporates)
from v0.ui.components.serializers import CompanyFloorSerializer, CorporateBuildingWingSerializer


class SupplierEducationalInstituteSerializer(ModelSerializer):
    class Meta:
        model = SupplierEducationalInstitute
        fields = '__all__'


class AddressMasterSerializer(ModelSerializer):
    class Meta:
        model = AddressMaster
        fields = '__all__'


class SupplierMasterSerializer(ModelSerializer):
    address_supplier = AddressMasterSerializer(read_only=True)
    class Meta:
        model = SupplierMaster
        fields = '__all__'


class SupplierHordingSerializer(ModelSerializer):
    class Meta:
        model = SupplierHording
        fields = '__all__'


class UICorporateSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeCorporate
        fields = '__all__'


class UISalonSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeSalon
        fields = '__all__'


class UIGymSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeGym
        fields = '__all__'


class BusShelterSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeBusShelter
        fields = '__all__'


class CorporateCompanyDetailsSerializer(ModelSerializer):
    class Meta:
        model = CorporateCompanyDetails
        fields = '__all__'


class SupplierAmenitiesMapSerializer(ModelSerializer):

    class Meta:
        model = SupplierAmenitiesMap
        fields = '__all__'
        depth = 1

class CorporateCompanySerializer(ModelSerializer):
    # for saving details of comapny with their building wing and floors /corporate/{{corporate_id}}/companyInfo
    listOfFloors = CompanyFloorSerializer(source='get_floors', many=True)

    class Meta:
        model = CorporateCompanyDetails
        fields = '__all__'


class CorporateParkCompanySerializer(ModelSerializer):
    # for saving details of comapny with their building wing and floors /corporate/{{corporate_id}}/companyInfo
    companyDetailList = CorporateCompanySerializer(source='get_company_details', many=True)

    class Meta:
        model = CorporateParkCompanyList
        fields = '__all__'


class CorporateParkCompanyListSerializer(ModelSerializer):
    class Meta:
        model = CorporateParkCompanyList
        fields = '__all__'


class CorporateBuildingGetSerializer(ModelSerializer):
    wingInfo = CorporateBuildingWingSerializer(source='get_wings', many=True)

    class Meta:
        model = CorporateBuilding
        fields = '__all__'


class SupplierTypeSocietySerializer(ModelSerializer):
    supplier_type = serializers.SerializerMethodField()
    class Meta:
        model = SupplierTypeSociety
        fields = '__all__'
    
    def get_supplier_type(self, obj):
        return 'RS'


class SupplierTypeSocietySerializer2(ModelSerializer):
    supplier_type = serializers.SerializerMethodField()
    class Meta:
        model = SupplierTypeSociety
        fields = '__all__'
    
    def get_supplier_type(self, obj):
        return 'RS'


class CorporateBuildingSerializer(ModelSerializer):
    class Meta:
        model = CorporateBuilding
        fields = '__all__'


class SupplierTypeCodeSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeCode
        fields = '__all__'


class SupplierTypeRetailShopSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeRetailShop
        fields = '__all__'


class SupplierTypeBusShelterSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeBusShelter
        fields = '__all__'


class SupplierTypeGymSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeGym
        fields = '__all__'


class SupplierTypeSalonSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeSalon
        fields = '__all__'


class SupplierTypeCorporateSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeCorporate
        fields = '__all__'


class SupplierInfoSerializer(ModelSerializer):
    class Meta:
        model = SupplierInfo
        fields = '__all__'


class RetailShopSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeRetailShop
        fields = '__all__'


class BusDepotSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeBusDepot
        fields = '__all__'

class SupplierBusSerializer(ModelSerializer):
    class Meta:
        model = SupplierBus
        fields = '__all__'

class SupplierGantrySerializer(ModelSerializer):
    class Meta:
        model = SupplierGantry
        fields = '__all__'

class SupplierRadioChannelSerializer(ModelSerializer):
    class Meta:
        model = SupplierRadioChannel
        fields = '__all__'

class SupplierTvChannelSerializer(ModelSerializer):
    class Meta:
        model = SupplierTvChannel
        fields = '__all__'

class SupplierCorporatesSerializer(ModelSerializer):
    class Meta:
        model = SupplierTvChannel
        fields = '__all__'

class SupplierHospitalSerializer(ModelSerializer):
    class Meta:
        model = SupplierTvChannel
        fields = '__all__'
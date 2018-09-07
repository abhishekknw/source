from rest_framework.serializers import ModelSerializer
from models import (SupplierTypeSociety, SupplierTypeCode, SupplierTypeRetailShop, SupplierTypeBusShelter,
                    SupplierTypeGym, SupplierTypeSalon, SupplierTypeCorporate, SupplierInfo, CorporateBuilding,
                    CorporateParkCompanyList, CorporateCompanyDetails, SupplierTypeBusDepot, SupplierAmenitiesMap)
from v0.ui.components.serializers import CompanyFloorSerializer, CorporateBuildingWingSerializer

class UICorporateSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeCorporate


class UISalonSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeSalon


class UIGymSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeGym


class BusShelterSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeBusShelter

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
    class Meta:
        model = SupplierTypeSociety
        fields = ('supplier_id', 'society_name', 'society_address1', 'society_address2', 'society_zip', 'society_city',
                  'society_state', 'society_longitude', 'society_locality', 'society_subarea', 'society_latitude', 'society_location_type',
                  'society_type_quality', 'society_type_quantity', 'flat_count', 'flat_avg_rental_persqft', 'flat_sale_cost_persqft',
                  'tower_count', 'payment_details_available', 'age_of_society','total_tenant_flat_count','landmark','feedback',
                  'name_for_payment','bank_name','ifsc_code','account_no',
                  )

class SupplierTypeSocietySerializer2(ModelSerializer):
    class Meta:
        model = SupplierTypeSociety
        fields = '__all__'

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

class BusDepotSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeBusDepot
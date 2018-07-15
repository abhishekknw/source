from rest_framework.serializers import ModelSerializer
from models import (SupplierTypeSociety, SupplierTypeCode, SupplierTypeRetailShop, SupplierTypeBusShelter,
                    SupplierTypeGym, SupplierTypeSalon, SupplierTypeCorporate, SupplierInfo)


class SupplierTypeSocietySerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeSociety
        fields = ('supplier_id', 'society_name', 'society_address1', 'society_address2', 'society_zip', 'society_city',
                  'society_state', 'society_longitude', 'society_locality', 'society_subarea', 'society_latitude', 'society_location_type',
                  'society_type_quality', 'society_type_quantity', 'flat_count', 'flat_avg_rental_persqft', 'flat_sale_cost_persqft',
                  'tower_count', 'payment_details_available', 'age_of_society','total_tenant_flat_count','landmark','feedback',
                  )


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
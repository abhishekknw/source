from rest_framework.serializers import ModelSerializer
from models import Organisation, OrganisationMap
from v0.ui.base.serializers import BaseModelPermissionSerializer


class OrganisationSerializer(BaseModelPermissionSerializer):

    class Meta:
        model = Organisation
        fields = '__all__'


class OrganisationMapNestedSerializer(ModelSerializer):
    """

    """
    first_organisation = OrganisationSerializer()
    second_organisation = OrganisationSerializer()

    class Meta:
        model = OrganisationMap
        fields = '__all__'

class OrganisationSerializer(ModelSerializer):

    class Meta:
        model = Organisation
        fields = '__all__'
from rest_framework.serializers import ModelSerializer
from models import UserProfile, BaseUser
from v0.serializers import GroupSerializer, PermissionsSerializer
from v0.ui.account.serializers import ProfileNestedSerializer

class UserProfileSerializer(ModelSerializer):
    # user1 = UserSerializer(source='get_user')
    class Meta:
        model = UserProfile
        fields = '__all__'
        # read_only_fields = (
    #    'user1'
    # )


class UserSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'


class BaseUserSerializer(ModelSerializer):
    """
    You can only write a password. Not allowed to read it. Hence password is in extra_kwargs dict.
    when creating a BaseUser instance we want password to be saved by .set_password() method, hence overwritten to
    do that.
    When updating the BaseUser, we never update the password. There is a separate api for updating password.
    """
    groups = GroupSerializer(read_only=True, many=True)
    user_permissions = PermissionsSerializer(read_only=True, many=True)
    profile = ProfileNestedSerializer()

    def create(self, validated_data):
        """
        Args:
            validated_data: the data that is used to be create the user.

        Returns: sets the password of the user when it's created.
        """

        # get the password
        password = validated_data['password']
        # delete it from the validated_data because we do not want to save it as raw password
        del validated_data['password']
        user = self.Meta.model.objects.create(**validated_data)
        # save password this way
        user.set_password(password)
        # save profile
        user.save()
        # return
        return user

    class Meta:
        model = BaseUser
        fields = (
        'id', 'first_name', 'last_name', 'email', 'user_code', 'username', 'mobile', 'password', 'is_superuser',
        'groups', 'user_permissions', 'profile')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class BaseUserUpdateSerializer(ModelSerializer):
    """
    specific to updating the USER model
    """

    def update(self, instance, validated_data):
        """
        Args:
            instance: The instance to be updated
            validated_data: a dict having data to be updated
        Returns: an updated instance
        """
        # if password provided, then update the password
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            del validated_data['password']

        for key, value in validated_data.iteritems():
            setattr(instance, key, value)

        instance.save()
        # return the updated instance
        return instance

    class Meta:
        model = BaseUser
        fields = ('id', 'first_name', 'last_name', 'email', 'user_code', 'username', 'mobile', 'is_superuser', 'groups',
                  'user_permissions', 'profile', 'role')
from django.contrib.auth.models import User
from rest_framework import serializers

from backend.services.zabbix_service.zabbix_packages import ZabbixHelper
from .models import UserSystem, APIEndpoint, UserType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserSystemSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserSystem
        fields = [
            'user', 'zabbix_server_url', 'zabbix_username',
            'zabbix_password', 'zabbix_host_name', 'user_type'
        ]
        extra_kwargs = {
            'zabbix_password': {'write_only': True},
        }

    def validate(self, data):
        if self.context.get("is_admin_creation"):
            try:
                ZabbixHelper(
                    url=data['zabbix_server_url'],
                    user=data['zabbix_username'],
                    password=data['zabbix_password'],
                    host_name=data['zabbix_host_name']
                )
            except ValueError as e:
                raise serializers.ValidationError({"zabbix_credentials": str(e)})
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)

        if validated_data.get("user_type") == UserType.USER and 'admin' in validated_data:
            admin = validated_data.pop('admin')
            validated_data['zabbix_server_url'] = admin.zabbix_server_url
            validated_data['zabbix_username'] = admin.zabbix_username
            validated_data['zabbix_password'] = admin.zabbix_password
            validated_data['zabbix_host_name'] = admin.zabbix_host_name

        # Create UserSystem instance with associated user
        usersystem = UserSystem.objects.create(user=user, **validated_data)
        return usersystem


class APIEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIEndpoint
        fields = ['id', 'name', 'path', 'method']


class SignupSerializer(serializers.ModelSerializer):
    zabbix_username = serializers.CharField(max_length=255)
    zabbix_password = serializers.CharField(max_length=255, write_only=True)  # Hide password in response
    zabbix_server_url = serializers.CharField(max_length=255)
    zabbix_host_name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password', 'zabbix_server_url', 'zabbix_host_name', 'zabbix_username', 'zabbix_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Validate Zabbix credentials
        try:
            ZabbixHelper(
                url=data['zabbix_server_url'],
                user=data['zabbix_username'],
                password=data['zabbix_password'],
                host_name=data['zabbix_host_name']
            )
        except ValueError as e:
            raise serializers.ValidationError({"zabbix_credentials": str(e)})

        return data

    def create(self, validated_data):

        # TODO: handle what the url going to look like, get it by hand for now

        user = User.objects.create_user(

            username=validated_data['username'],
            password=validated_data['password']

        )

        UserSystem.objects.create(
            user=user,
            zabbix_username=validated_data['zabbix_username'],
            zabbix_password=validated_data['zabbix_password'],
            zabbix_server_url=validated_data['zabbix_server_url'],
            zabbix_host_name=validated_data['zabbix_host_name']
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSystem
        fields = ['zabbix_server_url', 'zabbix_host_name']


class UpdateZabbixSettingsSerializer(serializers.ModelSerializer):
    zabbix_username = serializers.CharField(max_length=255, required=False)
    zabbix_password = serializers.CharField(max_length=255, write_only=True, required=False)
    zabbix_server_url = serializers.CharField(max_length=255, required=False)
    zabbix_host_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = UserSystem
        fields = ['zabbix_username', 'zabbix_password', 'zabbix_server_url', 'zabbix_host_name']
        extra_kwargs = {'zabbix_password': {'required': False}}

    def validate(self, data):
        # Validate Zabbix credentials
        if 'zabbix_server_url' in data and 'zabbix_username' in data and 'zabbix_password' in data:
            try:
                ZabbixHelper(
                    url=data['zabbix_server_url'],
                    user=data['zabbix_username'],
                    password=data['zabbix_password'],
                    host_name=data.get('zabbix_host_name', '')
                )
            except ValueError as e:
                raise serializers.ValidationError({"zabbix_credentials": str(e)})

        return data

    def update(self, instance, validated_data):
        instance.zabbix_username = validated_data.get('zabbix_username', instance.zabbix_username)
        instance.zabbix_server_url = validated_data.get('zabbix_server_url', instance.zabbix_server_url)
        instance.zabbix_host_name = validated_data.get('zabbix_host_name', instance.zabbix_host_name)

        # Only update the password if it's provided
        if 'zabbix_password' in validated_data:
            instance.zabbix_password = validated_data['zabbix_password']

        instance.save()
        return instance
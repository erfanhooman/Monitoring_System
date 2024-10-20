from django.contrib.auth.models import User
from rest_framework import serializers

from backend.services.zabbix_service.zabbix_packages import ZabbixHelper
from .models import UserSystem


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

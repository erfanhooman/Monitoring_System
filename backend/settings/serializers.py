import logging
import os

from backend.services.zabbix_service.zabbix_packages import ZabbixHelper
from django.contrib.auth.models import User
from django.core.files import File
from rest_framework import serializers

from .models import UserSystem, Permissions
from .utils.client_setup import create_openvpn_client

logger = logging.getLogger("ms")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        success, bundle_path = create_openvpn_client(validated_data['username'])

        if success:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password']
            )


            user_system = UserSystem.objects.create(
                user=user,
                user_type="admin"
            )

            with open(bundle_path, 'rb') as bundle_file:
                user_system.script_file.save(f"{validated_data['username']}_bundle.tar.gz", File(bundle_file))

            os.remove(bundle_path)

            return user
        else:
            raise serializers.ValidationError("Unable to create a bundle")




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class UserSystemSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserSystem
        fields = [
            'user', 'id', 'zabbix_server_url', 'zabbix_username',
            'zabbix_password', 'zabbix_host_name', 'user_type', 'active'
        ]
        extra_kwargs = {
            'user_type': {'read_only': True},
            'id': {'read_only': True},
        }

    def validate(self, data):
        zabbix_server_url = data.get('zabbix_server_url') or self.instance.zabbix_server_url
        zabbix_username = data.get('zabbix_username') or self.instance.zabbix_username
        zabbix_password = data.get('zabbix_password') or self.instance.zabbix_password
        zabbix_host_name = data.get('zabbix_host_name') or self.instance.zabbix_host_name

        try:
            if zabbix_server_url and zabbix_username and zabbix_password and zabbix_host_name:
                ZabbixHelper(
                    url=zabbix_server_url,
                    user=zabbix_username,
                    password=zabbix_password,
                    host_name=zabbix_host_name
                )
            return data
        except ValueError as e:
            raise serializers.ValidationError({"zabbix_credentials": str(e)})

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['id', 'name']

class SubUserSystemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = UserSystem
        fields = [
            'user', 'id', 'user_type', 'active', 'permissions'
        ]
        extra_kwargs = {
            'user_type': {'read_only': True},
            'id': {'read_only': True},
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        permissions_data = validated_data.pop('permissions', None)

        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        if permissions_data:
            instance.permissions.set(permissions_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class UpdateZabbixSettingsSerializer(serializers.ModelSerializer):
    zabbix_username = serializers.CharField(max_length=255)
    zabbix_password = serializers.CharField(max_length=255)
    zabbix_server_url = serializers.CharField(max_length=255)
    zabbix_host_name = serializers.CharField(max_length=255)

    class Meta:
        model = UserSystem
        fields = ['zabbix_username', 'zabbix_password', 'zabbix_server_url', 'zabbix_host_name']
        extra_kwargs = {'zabbix_password': {'required': False}}

    def validate(self, data):

        zabbix_server_url = data.get('zabbix_server_url') or self.instance.zabbix_server_url
        zabbix_username = data.get('zabbix_username') or self.instance.zabbix_username
        zabbix_password = data.get('zabbix_password') or self.instance.zabbix_password
        zabbix_host_name = data.get('zabbix_host_name') or self.instance.zabbix_host_name

        try:
            ZabbixHelper(
                url=zabbix_server_url,
                user=zabbix_username,
                password=zabbix_password,
                host_name=zabbix_host_name
            )
            return data
        except ValueError as e:
            raise serializers.ValidationError({"zabbix_credentials": str(e)})

    def update(self, instance, validated_data):
        instance.zabbix_username = validated_data.get('zabbix_username', instance.zabbix_username)
        instance.zabbix_server_url = validated_data.get('zabbix_server_url', instance.zabbix_server_url)
        instance.zabbix_host_name = validated_data.get('zabbix_host_name', instance.zabbix_host_name)

        if 'zabbix_password' in validated_data:
            instance.zabbix_password = validated_data['zabbix_password']

        instance.save()
        return instance


class SignupSubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'id']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        admin = self.context['request'].user.usersystem
        UserSystem.objects.create(
            user=user,
            user_type="user",
            admin=admin
        )

        return user

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from backend.messages import mt
from backend.utils import create_response
from .models import UserSystem, UserType, UserPermission, APIEndpoint
from .permissions import IsSuperAdmin, IsAdmin
from .serializers import SignupSerializer, LoginSerializer, UpdateZabbixSettingsSerializer, UserSystemSerializer


class AdminManagementView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        admin_count = UserSystem.objects.filter(user_type=UserType.ADMIN).count()
        user_count = UserSystem.objects.filter(user_type=UserType.USER).count()
        admins = UserSystem.objects.filter(user_type=UserType.ADMIN)
        serializer = UserSystemSerializer(admins, many=True)

        data = {
            'total_admins': admin_count,
            'total_users': user_count,
            'users': serializer.data,
        }  # TODO: also query the user and their permission, for now lets go

        return create_response(success=True, status=status.HTTP_200_OK, data=data, message=mt[200])

    def post(self, request):
        serializer = UserSystemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type=UserType.ADMIN)
            return create_response(success=True, status=status.HTTP_201_CREATED, data=serializer.data, message=mt[201])
        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[404])


class AdminUserManagement(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        """
        Get the list of subusers for the admin and their permissions.
        """
        subusers = UserSystem.objects.filter(admin=request.user.usersystem)
        subuser_data = []

        for subuser in subusers:
            permissions = UserPermission.objects.filter(user=subuser).values_list('endpoint__name', flat=True)
            serialized_subuser = UserSystemSerializer(subuser).data
            serialized_subuser['permissions'] = list(permissions)
            subuser_data.append(serialized_subuser)

        return create_response(success=True, status=status.HTTP_200_OK, data=subuser_data, message=mt[200])

    def post(self, request):
        """
        Update a subuser's details and change their permissions.
        """
        subuser_id = request.data.get('subuser_id')
        subuser = get_object_or_404(UserSystem, id=subuser_id, admin=request.user.usersystem)

        # Update user details
        serializer = UserSystemSerializer(subuser, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update permissions if provided
            if 'permissions' in request.data:
                endpoint_ids = request.data['permissions']
                UserPermission.objects.filter(user=subuser).delete()

                endpoints = APIEndpoint.objects.filter(id__in=endpoint_ids)
                for endpoint in endpoints:
                    UserPermission.objects.create(user=subuser, endpoint=endpoint)

            return create_response(success=True, status=status.HTTP_200_OK, data=serializer.data, message=mt[200])

        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[404])


class SignupSubUserView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        """
        Add a new subuser for the admin.
        """
        serializer = UserSystemSerializer(data=request.data, context={"is_admin_creation": False})
        if serializer.is_valid():
            serializer.save(
                user_type=UserType.USER,
                admin=request.user.usersystem
            )
            return create_response(success=True, status=status.HTTP_201_CREATED, data=serializer.data, message=mt[201])

        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[404])

class SignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Signup",
        operation_description="Sign up to monitor your system.",
        request_body=SignupSerializer,
        responses={
            200: openapi.Response(
                description="Sign up successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "user created, successfully",
                        "data": {
                            "username": "system username that set for monitoring system",
                            "password": "system password that set for monitoring system",
                            "zabbix_server_url": "server url for remote access",
                            "zabbix_host_name": "zabbix host name set for the remote one",
                            "zabbix_username": "zabbix username",
                            "zabbix_password": "zabbix password"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "The Reason of the Error",
                        "data": {
                            "field with problem": [
                                "the problem of it"
                            ]
                        }
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(success=True, status=status.HTTP_201_CREATED, message=mt[201],
                                   data=serializer.validated_data)
        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, message=mt[404],
                               data=serializer.errors)


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Login and get the Token",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="login successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "user logged in, successfully",
                        "data": {
                            "access": "access token (life time: 60min)",
                            "refresh": "refresh token (life time: 30days)"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "The Reason of the Error"
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                data = {
                    "refresh": str(RefreshToken.for_user(user)),
                    "access": str(AccessToken.for_user(user))
                }
                return create_response(success=True, status=status.HTTP_200_OK, data=data)
            return create_response(success=False, status=status.HTTP_401_UNAUTHORIZED, message=mt[431])
        return create_response(status=status.HTTP_401_UNAUTHORIZED, success=False, data=serializer.errors)


class UpdateZabbixSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Update Zabbix Settings",
        operation_description="Update your Zabbix monitoring settings.",
        request_body=UpdateZabbixSettingsSerializer,
        responses={
            200: openapi.Response(
                description="Zabbix settings updated successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Zabbix settings updated successfully.",
                        "data": {
                            "zabbix_server_url": "https://your-zabbix-server-url.com",
                            "zabbix_username": "new_username",
                            "zabbix_password": "new_password",
                            "zabbix_host_name": "new_host_name"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid input data",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "The reason for the error",
                        "data": {
                            "field_with_issue": [
                                "error description"
                            ]
                        }
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - UserSystem settings not found or invalid credentials",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "UserSystem settings not found."
                    }
                }
            )
        }
    )
    def post(self, request):
        user = request.user
        user_system = UserSystem.objects.filter(user=user).first()

        if not user_system:
            return create_response(success=False, status=status.HTTP_401_UNAUTHORIZED, message=mt[430])

        serializer = UpdateZabbixSettingsSerializer(user_system, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return create_response(success=True, status=status.HTTP_200_OK, data=serializer.validated_data,
                                   message=mt[200])

        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[404])

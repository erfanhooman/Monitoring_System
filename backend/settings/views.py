from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from backend.messages import mt
from backend.utils import create_response
from .serializers import SignupSerializer, LoginSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Signup",
        operation_description="Sign up to monitor your system.",
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
            return create_response(success=True, message=mt[201], data=serializer.validated_data)
        return create_response(success=False, message=mt[404],
                               data=serializer.errors)

        # TODO: bad request fix the create response


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Login and get the Token",
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
                return create_response(data=data, success=True)
            return create_response(data={"error": "Invalid credentials"}, success=False)
        return create_response(data=serializer.errors, success=False)

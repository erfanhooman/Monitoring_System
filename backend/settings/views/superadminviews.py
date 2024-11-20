from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from backend.messages import mt
from backend.utils import create_response
from ..models import UserSystem, UserType
from ..permissions import IsSuperAdmin
from ..serializers import SignupSerializer, UserSystemSerializer


class AdminSignupView(APIView):
    permission_classes = [IsSuperAdmin]

    @swagger_auto_schema(
        operation_summary="Sign up a new user by Super Admin",
        operation_description="Allows the Super Admin to create new users by providing the required details.",
        request_body=SignupSerializer,
        responses={
            201: openapi.Response(description="User created successfully"),
            400: openapi.Response(description="Invalid input or data"),
        },
    )
    def post(self, request):
        """
        signup new users by super admin
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(success=True, status=status.HTTP_201_CREATED, data=serializer.data, message=mt[201])
        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[414])


class AdminManagementView(APIView):
    permission_classes = [IsSuperAdmin]

    @swagger_auto_schema(
        operation_summary="Retrieve user or admin information",
        operation_description=(
            "Fetch user details based on `user_id` provided in the request body. "
            "If no `user_id` is provided, fetch a list of all admins and the total admin count."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the user to retrieve details for (optional for fetching all admins)."
                ),
            },
            required=[],
        ),
        responses={
            200: openapi.Response(
                description="User information retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "total_users": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "users": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    },
                ),
            ),
            404: openapi.Response(description="User not found"),
        },
    )
    def get(self, request):
        user_id = request.data.get("user_id")
        if user_id:
            try:
                user_system = UserSystem.objects.get(id=user_id)
                serializer = UserSystemSerializer(user_system)
                data = serializer.data
            except UserSystem.DoesNotExist:
                return create_response(success=False, status=status.HTTP_404_NOT_FOUND, message=mt[403])
        else:
            admin_count = UserSystem.objects.filter(user_type=UserType.ADMIN).count()
            admins = UserSystem.objects.filter(user_type=UserType.ADMIN)
            serializer = UserSystemSerializer(admins, many=True)

            data = {
                'total_users': admin_count,
                'users': serializer.data,
            }

        return create_response(success=True, status=status.HTTP_200_OK, data=data, message=mt[200])

    @swagger_auto_schema(
        operation_summary="Update user details",
        operation_description="Allows updating specific user details. `user_id` must be provided in the request body.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the user to update (required).",
                ),
                **UserSystemSerializer().fields
            },
            required=["user_id"],
        ),
        responses={
            200: openapi.Response(description="User details updated successfully", schema=UserSystemSerializer),
            400: openapi.Response(description="Invalid input or data"),
            404: openapi.Response(description="User not found"),
        },
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, message=mt[415])

        try:
            user_system = UserSystem.objects.get(id=user_id)
        except UserSystem.DoesNotExist:
            return create_response(success=False, status=status.HTTP_404_NOT_FOUND, message=mt[416])

        serializer = UserSystemSerializer(user_system, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return create_response(success=True, status=status.HTTP_200_OK, data=serializer.data, message=mt[200])
        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[414])
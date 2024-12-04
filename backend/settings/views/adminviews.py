from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from backend.messages import mt
from backend.utils import create_response, permission_for_view
from ..models import UserSystem, UserType, Permissions
from ..serializers import SignupSubUserSerializer, SubUserSystemSerializer


class UserSignup(APIView):
    permission_classes = [permission_for_view('USER')]

    @swagger_auto_schema(
        operation_summary="Sign up a new subuser",
        operation_description=(
                "Allows an admin to sign up a new subuser. The new subuser will be associated with the admin "
                "and inherit shared configurations like `zabbix_server_url`, but will have a unique username and password."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Username for the new subuser (required)."
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password for the new subuser (required)."
                ),
            },
            required=["username", "password"],
        ),
        responses={
            201: openapi.Response(
                description="Subuser successfully created.",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User created successfully.",
                        "status": 201,
                        "data": {
                            "username": "new_subuser",
                            "id": 123,
                        },
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid input or validation error.",
                examples={
                    "application/json": {
                        "success": False,
                        "status": 400,
                        "data": {"username": ["This field is required."]},
                        "message": "Validation error."
                    }
                }
            ),
        },
    )
    def post(self, request):
        """
        sign up new subuser by admin
        """
        serializer = SignupSubUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return create_response(success=True, status=status.HTTP_201_CREATED, data=serializer.data, message=mt[201])
        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[414])


class UserManagementView(APIView):
    permission_classes = [permission_for_view('USER'),]

    @swagger_auto_schema(
        operation_summary="Retrieve subuser information",
        operation_description=(
            "Fetch user details based on `user_id` provided in the request body. "
            "If no `user_id` is provided, fetch a list of all sub-users and the total sub-users count."
        ),
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="ID of the user to retrieve details for (optional for fetching all sub-users)",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
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
                user_system = UserSystem.objects.get(id=user_id, admin=request.user.usersystem.id)
                serializer = SubUserSystemSerializer(user_system)
                data = serializer.data
            except UserSystem.DoesNotExist:
                return create_response(success=False, status=status.HTTP_404_NOT_FOUND, message=mt[403])
        else:
            user_count = UserSystem.objects.filter(admin=request.user.usersystem.id).count()
            sub_users = UserSystem.objects.filter(admin=request.user.usersystem.id)
            serializer = SubUserSystemSerializer(sub_users, many=True)

            data = {
                'total_users': user_count,
                'users': serializer.data,
            }

        return create_response(success=True, status=status.HTTP_200_OK, data=data, message=mt[200])

    @swagger_auto_schema(
        operation_summary="Update subusers details",
        operation_description="Allows updating specific user details. `user_id` must be provided in the request body.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the user to update (required).",
                ),
                "user": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "username": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="The username of the user.",
                        ),
                        "password": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Password of the user.",
                            write_only=True
                        ),
                    }
                ),
                "active": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Is the user active?",
                )
            },
            required=["user_id"],
        ),
        responses={
            200: openapi.Response(description="User details updated successfully", schema=SubUserSystemSerializer),
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

        serializer = SubUserSystemSerializer(user_system, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return create_response(success=True, status=status.HTTP_200_OK, data=serializer.data, message=mt[200])
        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[414])


class ModifyUserPermissionsView(APIView):
    permission_classes = [permission_for_view('USER'),]

    @swagger_auto_schema(
        operation_summary="Update subusers details",
        operation_description="Allows updating specific user details. `user_id` must be provided in the request body. The `permissions` field should contain the permissions the user can access. See below for the list of permissions.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the user to update (required).",
                ),
                "permissions": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=[
                            "DASHBOARD",
                            "CPU",
                            "RAM",
                            "DISK",
                            "NETWORK",
                            "GENERAL",
                            "FS",
                            "SETTINGS",
                            "USER"
                        ]
                    ),
                    description=(
                            "List of permissions that the user can access. "
                            "Available options are: \n"
                            "- **DASHBOARD**: Access the dashboard.\n"
                            "- **CPU**: Access CPU details.\n"
                            "- **RAM**: Access RAM details.\n"
                            "- **DISK**: Access disk details.\n"
                            "- **NETWORK**: Access network details.\n"
                            "- **GENERAL**: Access general details.\n"
                            "- **FS**: Access file system details.\n"
                            "- **SETTINGS**: Access settings.\n"
                            "- **USER**: user managment.\n"
                    ),
                )
            },
            required=["user_id"],
        ),
        responses={
            200: openapi.Response(
                description="User permissions updated successfully",
                schema=SubUserSystemSerializer
            ),
            400: openapi.Response(description="Invalid input or data"),
            404: openapi.Response(description="User not found"),
        },
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, message=mt[415])

        try:
            user_system = UserSystem.objects.get(id=user_id, admin=request.user.usersystem)
        except UserSystem.DoesNotExist:
            return create_response(success=False, status=status.HTTP_404_NOT_FOUND, message=mt[416])

        permissions = request.data.get("permissions", [])
        permission_objs = Permissions.objects.filter(codename__in=permissions)

        user_system.permissions.set(permission_objs)
        user_system.save()

        serializer = SubUserSystemSerializer(user_system)
        return create_response(success=True, status=status.HTTP_200_OK, data=serializer.data, message=mt[200])
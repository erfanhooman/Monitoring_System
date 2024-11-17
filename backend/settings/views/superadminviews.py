from rest_framework import status
from rest_framework.views import APIView

from backend.messages import mt
from backend.utils import create_response
from ..models import UserSystem, UserType
from ..permissions import IsSuperAdmin
from ..serializers import SignupSerializer, UserSystemSerializer


class AdminSignup(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request):
        """
        signup new users by super admin
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(success=True, status=status.HTTP_201_CREATED, data=serializer.data, message=mt[201])
        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[404])


class AdminManagementView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request, user_id=None):
        if user_id:
            try:
                user_system = UserSystem.objects.get(id=user_id)
                serializer = UserSystemSerializer(user_system)
                data = serializer.data
            except UserSystem.DoesNotExist:
                return create_response(success=False, status=status.HTTP_404_NOT_FOUND, message=mt[403])
        else:
            user_count = UserSystem.objects.filter(user_type=UserType.USER).count()
            admins = UserSystem.objects.filter(user_type=UserType.ADMIN)
            serializer = UserSystemSerializer(admins, many=True)

            data = {
                'total_users': user_count,
                'users': serializer.data,
            }

        return create_response(success=True, status=status.HTTP_200_OK, data=data, message=mt[200])

    def post(self, request, user_id=None):
        if not user_id:
            return create_response(success=False, status=status.HTTP_404_NOT_FOUND, message=mt[405])

        try:
            user_system = UserSystem.objects.get(id=user_id)
        except UserSystem.DoesNotExist:
            return create_response(success=False, status=status.HTTP_404_NOT_FOUND, message=mt[404])

        serializer = UserSystemSerializer(user_system, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return create_response(success=True, status=status.HTTP_200_OK, data=serializer.data, message=mt[200])
        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[404])

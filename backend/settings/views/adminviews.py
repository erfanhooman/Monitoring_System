from rest_framework.views import APIView
from rest_framework import status

from ..permissions import IsAdmin
from ..serializers import SignupSubUserSerializer
from backend.utils import create_response
from backend.messages import mt

class UserSignup(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        """
        sign up new subuser by admin
        """
        serializer = SignupSubUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return create_response(success=True, status=status.HTTP_201_CREATED, data=serializer.data, message=mt[201])
        return create_response(success=False, status=status.HTTP_400_BAD_REQUEST, data=serializer.errors,
                               message=mt[404])
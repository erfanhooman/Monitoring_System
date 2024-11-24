import requests
from rest_framework import status
from rest_framework import status as st
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.permissions import IsAuthenticated
from .models import UserAlertPreference
from backend.utils import create_response
from backend.messages import mt


class ProblemReportView(APIView):
    def post(self, request):
        user = request.user
        item_key = request.data.get("item_key")
        status = request.data.get("status")
        value = request.data.get("value")

        if not item_key or not status:
            return Response({"error": "Invalid data"}, status=st.HTTP_400_BAD_REQUEST)

        send_user_notification(user, item_key, status, value)

        return Response({"message": "Report received"}, status=st.HTTP_200_OK)


def send_user_notification(user, item_key, status, value):
    message = f"Alert: {item_key} is in {status} status. Current value: {value}."
    print(f"NOTIFICATION: {user} - {message}")

#TODO: add a permission_for_view also to this one
class AlertPreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        item_key = request.data.get("item_key")
        alert_level = request.data.get("alert_level", "critical")
        enabled = request.data.get("enabled", True)

        if not item_key:
            return Response({"error": "item_key is required"}, status=status.HTTP_400_BAD_REQUEST)

        local_server_url = f"http://{user.usersystem.zabbix_server_url}:5000/internal/update_preferences/"
        payload = {
            "item_key": item_key,
            "enabled": enabled,
            "alert_level": alert_level,
        }
        headers = {"Authorization": "Bearer YOUR_SECURE_TOKEN"}

        try:
            response = requests.post(local_server_url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:

                preference, created = UserAlertPreference.objects.update_or_create(
                    user=user.usersystem,
                    item_key=item_key,
                    defaults={"enabled": enabled, "alert_level": alert_level},
                )

            else:
                return create_response(success=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=mt[506])
        except requests.exceptions.RequestException as e:
            return create_response(success=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=mt[506])

        return create_response(success=True, status=status.HTTP_200_OK, message=mt[200],
                               data={"item_key": item_key, "enabled": enabled})

    def get(self, request):
        preferences = UserAlertPreference.objects.filter(user=request.user.usersystem)
        data = [
            {
                "item_key": pref.item_key,
                "enabled": pref.enabled,
                "alert_level": pref.alert_level,
            }
            for pref in preferences
        ]
        return create_response(success=True, data=data, status=st.HTTP_200_OK)

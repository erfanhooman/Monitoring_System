from rest_framework import status as st
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserAlertPreference


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


class AlertPreferenceView(APIView):
    def get(self, request):
        preferences = UserAlertPreference.objects.filter(user=request.user)
        data = [
            {
                "item_key": pref.item_key,
                "enabled": pref.enabled,
                "alert_level": pref.alert_level,
            }
            for pref in preferences
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        item_key = request.data.get("item_key")
        alert_level = request.data.get("alert_level", "critical")
        enabled = request.data.get("enabled", True)

        if not item_key:
            return Response({"error": "item_key is required"}, status=status.HTTP_400_BAD_REQUEST)

        preference, created = UserAlertPreference.objects.update_or_create(
            user=user,
            item_key=item_key,
            defaults={"enabled": enabled, "alert_level": alert_level},
        )
        return Response(
            {"message": "Preference updated", "item_key": item_key, "enabled": enabled},
            status=status.HTTP_200_OK,
        )

import logging

import requests
from backend.messages import mt
from backend.utils import create_response, permission_for_view
from rest_framework import status as st
from rest_framework.response import Response
from rest_framework.views import APIView
from settings.permissions import IsAuthenticated

from .models import UserAlertPreference

logger = logging.getLogger("ms")

class ProblemReportView(APIView):
    def post(self, request):
        user = request.user
        item_key = request.data.get("item_key")
        status = request.data.get("status")
        value = request.data.get("value")

        if not item_key or not status:
            logging.warning("Invalid data received: Missing item_key or status.")
            return Response({"error": "item_key and status are required"}, status=st.HTTP_400_BAD_REQUEST)

        try:
            value = float(value)
        except (ValueError, TypeError):
            logging.warning(f"Invalid value received: {value}")
            return Response({"error": "Invalid value. Must be a number."}, status=st.HTTP_400_BAD_REQUEST)

        try:
            send_user_notification(user, item_key, status, value)
        except Exception as e:
            logging.exception(f"Error sending notification: {e}")
            return Response({"error": f"Error sending notification: {str(e)}"},
                            status=st.HTTP_500_INTERNAL_SERVER_ERROR)

        logging.info(f"Report processed successfully for {item_key} by {user}.")
        return Response({"message": "Report received"}, status=st.HTTP_200_OK)


# TODO: send notification after one time constantly, change to send the notification if its one time not constantly
def send_user_notification(user, item_key, status, value):
    message = f"Alert: {item_key} is in {status} status. Current value: {value}."
    try:
        logging.info(f"Sending notification: {user} - {message}")
        # TODO: Implement email or other notification logic here.
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")
        raise RuntimeError(f"Failed to send notification: {e}")


class AlertPreferenceView(APIView):
    permission_classes = [IsAuthenticated, permission_for_view('ALERT')]

    def post(self, request):
        user = request.user
        item_key = request.data.get("item_key")
        alert_level = request.data.get("alert_level", "critical")
        enabled = request.data.get("enabled", True)

        if not item_key:
            return create_response(success=True, status=st.HTTP_400_BAD_REQUEST, message=mt[414],
                                   data={"item_key": "item_key is required"})

        local_server_url = f"http://{user.usersystem.zabbix_server_url}:5000/internal/update_preferences/"
        logger.info(f"Sending alert for {item_key} preferences sync to Local Server")
        payload = {
            "item_key": item_key,
            "enabled": enabled,
            "alert_level": alert_level,
        }

        try:
            response = requests.post(local_server_url, json=payload, timeout=5, proxies={})
            if response.status_code == 200:
                preference, created = UserAlertPreference.objects.update_or_create(
                    user=user.usersystem,
                    item_key=item_key,
                    defaults={"enabled": enabled, "alert_level": alert_level},
                )
                logger.info(f"Preference successfully updated for user {user} and item {item_key}")
            else:
                logger.error(f"Local server error-{response.status_code} while trying to sync {item_key}")
                return create_response(success=False, status=st.HTTP_500_INTERNAL_SERVER_ERROR,
                                       message=mt[700])
        except requests.exceptions.RequestException as e:
            print(e)
            logger.error(f"Error communicating with the local server while trying to sync {item_key}")
            return create_response(success=False, status=st.HTTP_500_INTERNAL_SERVER_ERROR, message=mt[700])

        return create_response(success=True, status=st.HTTP_200_OK, message=mt[200], data={"item_key": item_key})

    def get(self, request):
        try:
            preferences = UserAlertPreference.objects.filter(user=request.user.usersystem)
            data = [
                {
                    "item_key": pref.item_key,
                    "enabled": pref.enabled,
                    "alert_level": pref.alert_level,
                }
                for pref in preferences
            ]
            logger.info(f"Retrieved {len(data)} preferences for user {request.user}.")
            return create_response(success=True, data=data, message=mt[200], status=st.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"Error retrieving Alert preferences: {e}")
            create_response(success=False, status=st.HTTP_500_INTERNAL_SERVER_ERROR, message=mt[500])

    def delete(self, request):
        user = request.user
        item_key = request.data.get("item_key")

        if not item_key:
            return create_response(success=True, status=st.HTTP_400_BAD_REQUEST, message=mt[414],
                                   data={"item_key": "item_key is required"})

        local_server_url = f"http://{user.usersystem.zabbix_server_url}:5000/internal/delete_preferences/"
        payload = {"item_key": item_key}

        try:
            response = requests.post(local_server_url, json=payload, timeout=5)
            if response.status_code == 200:
                deleted_count, _ = UserAlertPreference.objects.filter(user=user.usersystem, item_key=item_key).delete()

                if deleted_count > 0:
                    logger.info(f"Deleted preference {item_key} for user {user}.")
                    return create_response(success=True, status=st.HTTP_200_OK, message=mt[200],
                                           data={"deleted_item": item_key})
                else:
                    logger.warning(f"Preference {item_key} not found in database for user {user}.")
                    return create_response(success=False, status=st.HTTP_400_BAD_REQUEST, message=mt[400],
                                           data={item_key: "Preference not found in database"})
            else:
                logger.error(f"Local server error during deletion: {response.status_code} - {response.text}")
                return create_response(success=False, status=st.HTTP_500_INTERNAL_SERVER_ERROR, message=mt[700])

        except requests.exceptions.RequestException as e:
            logger.exception("Error communicating with the local server for deletion.")
            return create_response(success=False, status=st.HTTP_500_INTERNAL_SERVER_ERROR, message=mt[700])

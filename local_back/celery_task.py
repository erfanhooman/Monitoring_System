"""
periodic task to check alerts locally.
"""

from celery import Celery
import requests

from user_alert_prefrence import UserAlertPreference
from shared.zabbix_service.zabbix_packages import ZabbixHelper


app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def check_and_report():
    zabbix = ZabbixHelper()
    preferences = UserAlertPreference.select().where(UserAlertPreference.enabled == True)

    for pref in preferences:
        try:
            item_data = zabbix.get_item_data(pref.item_key)
            if item_data:
                value = float(item_data[0]['value'])
                thresholds = STATIC_CONFIG[pref.item_key]['value']
                status_function = STATUS_FUNCTIONS[pref.item_key]
                status = status_function(value, thresholds['normal'], thresholds['warning'])

                # Check if status matches alert level
                if status == pref.alert_level:
                    # Send a report to the server
                    report_to_server(pref.item_key, status, value)
        except Exception as e:
            print(f"Error processing {pref.item_key}: {e}")

def report_to_server(item_key, status, value):
    payload = {
        "item_key": item_key,
        "status": status,
        "value": value
    }
    response = requests.post("http://your-server-url/api/problem_report/", json=payload)
    print(f"Report sent: {response.status_code}")
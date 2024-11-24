"""
What are you afraid of losing,
    when nothing in the world actually belongs to you
        - Marcus Aurelius
"""

import json
import os

import requests

from celery_app import app
from shared.utils.status_functions import STATUS_FUNCTIONS
from shared.zabbix_service.zabbix_packages import ZabbixHelper
from user_alert_prefrence import UserAlertPreference

SERVER_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{SERVER_URL}/api/auth/login/"
REPORT_ENDPOINT = f"{SERVER_URL}/internal/problemreport/"
USERNAME = "erfan"
PASSWORD = "erfan"


def load_configurations(config_dir="shared/configs"):
    config = {}
    for file_name in os.listdir(config_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(config_dir, file_name)) as f:
                config.update(json.load(f))
    return config


# TODO: for security reason find good way to connect to zabbix
@app.task(name='celery_tasks.check_and_report')
def check_and_report():
    zabbix = ZabbixHelper(
        url="localhost",
        user="Admin",
        password="zabbix",
        host_name="Zabbix server"
    )
    config = load_configurations()
    preferences = UserAlertPreference.select().where(UserAlertPreference.enabled == True)
    for pref in preferences:
        try:
            metric_key = pref.item_key
            if metric_key not in config:
                print(f"Config for {metric_key} not found!")
                continue

            item_data = zabbix.get_item_data(pref.item_key)
            if item_data:
                value = float(item_data[0].get('lastvalue', None))
                thresholds = config[metric_key]['value']

                status_function = STATUS_FUNCTIONS.get(metric_key)
                if not status_function:
                    print(f"Status function for {metric_key} not found!")
                    continue

                status = status_function(value, thresholds['normal'], thresholds['warning'])

                if status == pref.alert_level:
                    report_to_server(metric_key, status, value, USERNAME, PASSWORD)
        except RuntimeError as e:
            print(f"Error processing {pref.item_key}: {e}")


def login_to_server(username, password):
    """Logs in to the server and retrieves an authentication token."""
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(LOGIN_ENDPOINT, json=payload)
        response.raise_for_status()
        token = response.json().get("data").get("access")
        if not token:
            raise ValueError("No token returned from server.")
        return token
    except requests.RequestException as e:
        print(f"Error logging in to server: {e}")
        return None


def report_to_server(item_key, status, value, username, password):
    """Reports a problem to the server using an authenticated request."""
    token = login_to_server(username, password)
    if not token:
        print("Unable to authenticate. Problem report not sent.")
        return

    payload = {
        "item_key": item_key,
        "status": status,
        "value": value
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(REPORT_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error reporting to server: {e}")


# TODO: refactor the code to best practice

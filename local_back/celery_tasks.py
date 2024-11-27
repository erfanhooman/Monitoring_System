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
from logging_config import get_logger

logging = get_logger(__name__)

SERVER_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{SERVER_URL}/api/auth/login/"
REPORT_ENDPOINT = f"{SERVER_URL}/internal/problemreport/"
USERNAME = "erfan"
PASSWORD = "erfan"

LOG_FILE = "local_client.log"

def load_configurations(config_dir="shared/configs"):
    config = {}
    try:
        for file_name in os.listdir(config_dir):
            if file_name.endswith(".json"):
                with open(os.path.join(config_dir, file_name)) as f:
                    config.update(json.load(f))
        logging.info("Configurations loaded successfully.")
    except FileNotFoundError as e:
        logging.error(f"Configuration directory not found: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in configuration files: {e}")
    except Exception as e:
        logging.exception(f"Unexpected error loading configurations: {e}")
    return config



# TODO: for security reason find good way to connect to zabbix
@app.task(name='celery_tasks.check_and_report')
def check_and_report():
    try:
        zabbix = ZabbixHelper(
            url="localhost",
            user="Admin",
            password="zabbix",
            host_name="Zabbix server"
        )
    except Exception as e:
        logging.error(f"Error initializing ZabbixHelper: {e}")
        return

    config = load_configurations()
    if not config:
        logging.warning("No configurations loaded. Exiting.")
        return

    try:
        preferences = UserAlertPreference.select().where(UserAlertPreference.enabled == True)
    except Exception as e:
        logging.error(f"Error querying preferences: {e}")
        return

    for pref in preferences:
        try:
            metric_key = pref.item_key
            logging.info(f"check status for {metric_key}")
            if metric_key not in config:
                logging.warning(f"Config for {metric_key} not found!")
                continue

            item_data = zabbix.get_item_data(pref.item_key)
            if not item_data or 'lastvalue' not in item_data[0]:
                logging.warning(f"No valid item data found for {metric_key}")
                continue

            value = float(item_data[0].get('lastvalue', 0))
            thresholds = config[metric_key]['value']

            status_function = STATUS_FUNCTIONS.get(metric_key)
            if not status_function:
                logging.warning(f"Status function for {metric_key} not found!")
                continue

            status = status_function(value, thresholds['normal'], thresholds['warning'])

            if pref.alert_level == "critical" and status == "critical":
                report_to_server(metric_key, status, value, USERNAME, PASSWORD)
            elif pref.alert_level == "warning" and status in ["warning", "critical"]:
                report_to_server(metric_key, status, value, USERNAME, PASSWORD)

        except Exception as e:
            logging.exception(f"Error processing {pref.item_key}: {e}")


def login_to_server(username, password):
    """Logs in to the server and retrieves an authentication token."""
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(LOGIN_ENDPOINT, json=payload)
        response.raise_for_status()
        token = response.json().get("data", {}).get("access")
        if not token:
            raise ValueError("No token returned from server.")
        logging.info("Authentication successful.")
        return token
    except requests.ConnectionError as e:
        logging.error(f"Connection error while logging in: {e}")
    except requests.HTTPError as e:
        logging.error(f"HTTP error during login: {e}")
    except ValueError as e:
        logging.error(f"Invalid server response: {e}")
    except Exception as e:
        logging.exception(f"Unexpected error during login: {e}")
    return None

def report_to_server(item_key, status, value, username, password):
    """Reports a problem to the server using an authenticated request."""
    token = login_to_server(username, password)
    if not token:
        logging.error("Unable to authenticate. Problem report not sent.")
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
        logging.info(f"Report sent successfully for {item_key}.")
    except requests.ConnectionError as e:
        logging.error(f"Connection error while reporting to server: {e}")
    except requests.HTTPError as e:
        logging.error(f"HTTP error during report: {e}")
    except Exception as e:
        logging.exception(f"Unexpected error during report: {e}")

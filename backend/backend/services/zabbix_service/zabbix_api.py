import json
import logging

import requests
from django.conf import settings

ZABBIX_URL = settings.ZABBIX_SERVER
ZABBIX_USER = settings.ZABBIX_USER
ZABBIX_PASSWORD = settings.ZABBIX_PASSWORD
ZABBIX_HOST_NAME = settings.ZABBIX_HOST_NAME

from .base import ZabbixAPIBase

logger = logging.getLogger("ms")


class ZabbixBuiltinAPI(ZabbixAPIBase):
    def __init__(self, url):
        self.url = url
        self.auth_token = None
        self.headers = {"Content-Type": "application/json-rpc"}
        try:
            requests.get(self.url)  # Test connection to Zabbix URL
        except Exception as e:
            logger.error(f"Connection error to Zabbix API: {str(e)}")
            raise ConnectionError(f"Failed to connect to Zabbix API at {url}")

    def login(self, username, password):
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": username,
                    "password": password
                },
                "id": 1
            }
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            if "result" not in result:
                raise PermissionError(f"Login failed: {result.get('error', {}).get('data', 'Unknown error')}")
            self.auth_token = result['result']
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to login to Zabbix API: {str(e)}")
            raise ConnectionError(f"Error connecting to Zabbix API: {str(e)}")
        except PermissionError as e:
            logger.warning(str(e))
            raise
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            raise ConnectionError("Internal login error")

    def get_host_id(self, host_name):
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": ["hostid", "host"],
                    "filter": {"host": [host_name]}
                },
                "id": 2,
                "auth": self.auth_token
            }
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            if not result.get('result'):
                logger.info(f"Host not found: {host_name}")
                raise ValueError(f"Host not found: {host_name}")
            return result['result'][0]['hostid']
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error retrieving host ID: {str(e)}")
            raise ConnectionError(f"Error retrieving host ID: {str(e)}")
        except ValueError as e:
            logger.warning(str(e))
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving host ID: {str(e)}")
            raise ConnectionError("Internal host retrieval error")

    def get_item(self, host_id, item):
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": ["itemid", "name", "key_"],
                    "hostids": host_id,
                    "search": {"key_": item}
                },
                "id": 3,
                "auth": self.auth_token
            }
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            print(result)
            if not result.get('result'):
                logger.info(f"Item not found: item={item}, host_id={host_id}")
                return []
            return result['result']
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error retrieving item: {str(e)}")
            raise ConnectionError(f"Error retrieving item: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error retrieving item: {str(e)}")
            raise ConnectionError("Internal item retrieval error")

    def get_item_history(self, item_id, history=0, limit=30):
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": history,
                    "itemids": item_id,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "limit": limit
                },
                "id": 4,
                "auth": self.auth_token
            }
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            if not result.get('result'):
                logger.info(f"No history found for item ID: {item_id}")
                return []
            return result['result']
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error retrieving item history: {str(e)}")
            raise ConnectionError(f"Error retrieving item history: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error retrieving item history: {str(e)}")
            raise ConnectionError("Internal history retrieval error")

    def logout(self):
        try:
            if self.auth_token:
                payload = {
                    "jsonrpc": "2.0",
                    "method": "user.logout",
                    "params": [],
                    "id": 5,
                    "auth": self.auth_token
                }
                response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
                response.raise_for_status()
                self.auth_token = None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error logging out of Zabbix API: {str(e)}")
            raise ConnectionError("Logout error")
        except Exception as e:
            logger.error(f"Unexpected error during logout: {str(e)}")
            raise ConnectionError("Internal logout error")


class ZabbixHelper:
    def __init__(self, url=ZABBIX_URL, user=ZABBIX_USER, password=ZABBIX_PASSWORD, host_name=ZABBIX_HOST_NAME):
        try:
            self.zabbix = ZabbixBuiltinAPI(f'http://{url}/zabbix/api_jsonrpc.php')
            self.zabbix.login(user, password)
            self.host_id = self.zabbix.get_host_id(host_name)
        except (PermissionError, ValueError, LookupError, ConnectionError) as e:
            raise ValueError(f"{str(e)}")

    def get_item_data(self, item_key):
        try:
            return self.zabbix.get_item(self.host_id, item_key)
        except (ValueError, LookupError, ConnectionError) as e:
            raise ValueError(f"'{item_key}': {str(e)}")

    def get_item_history(self, item_key):
        try:
            item = self.get_item_data(item_key)
            if item:
                return self.zabbix.get_item_history(item[0]['itemid'])
            raise ValueError(f"'{item_key}'")
        except (ValueError, LookupError, ConnectionError) as e:
            raise ValueError(f"'{item_key}': {str(e)}")

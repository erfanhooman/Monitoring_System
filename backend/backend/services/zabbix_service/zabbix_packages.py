import logging

from pyzabbix import ZabbixAPI, ZabbixAPIException
from requests.exceptions import ConnectionError as RequestsConnectionError
from django.conf import settings

from .base import ZabbixAPIBase
from backend.messages import mt

ZABBIX_URL = f'http://{settings.ZABBIX_SERVER}/zabbix/api_jsonrpc.php'
ZABBIX_USER = settings.ZABBIX_USER
ZABBIX_PASSWORD = settings.ZABBIX_PASSWORD
ZABBIX_HOST_NAME = settings.ZABBIX_HOST_NAME

logger = logging.getLogger("ms")

class ZabbixPackage(ZabbixAPIBase):
    def __init__(self, url):
        self.url = url
        try:
            self.zabbix = ZabbixAPI(url)
        except Exception as e:
            logger.info(f"{mt[420]}: {str(e)}")
            raise ConnectionError(f"{mt[420]}:{url}")  # connection error

    def login(self, username, password):
        try:
            self.zabbix.login(username, password)
        except ZabbixAPIException as e: # login error
            logger.warning(f"{mt[421]}: {str(e)}")
            raise PermissionError(f"{mt[421]}")
        except RequestsConnectionError as e:  # Wrong Url Error
            logger.info(f"{mt[428]}: {self.url}")
            raise ConnectionError(f"{mt[428]}:{self.url}")
        except Exception as e:
            logger.error(f"{str(e)}")
            raise ConnectionError(f"{mt[501]}")  # Internal Login error

    def get_host_id(self, host_name):
        try:
            host = self.zabbix.host.get(filter={"host": f"{host_name}"})
            if not host:
                logger.info(f"{mt[422]}: {host_name}")
                raise ValueError(f"{mt[422]}:{host_name}")  # host name not found error
            return host[0]['hostid']
        except ZabbixAPIException as e:
            logger.info(f"{mt[423]}: {str(e)}")
            raise LookupError(f"{mt[423]}: {host_name}")  # host problem error
        except ValueError as e:
            raise ValueError(f"{mt[423]}: {host_name}")
        except Exception as e:
            logger.error(f"{str(e)}")
            raise ConnectionError(f"{mt[502]}")  # internal get_host error

    def get_item(self, host_id, item):
        try:
            data = self.zabbix.item.get(hostids=host_id, filter={"key_": f"{item}"})
            if not data:
                # logger.info(f"{mt[424]}: item:{item}, host_id{host_id}")
                raise ValueError(f"{mt[424]} item:{item} : host_id:{host_id}")  # Item for this host id not found
            return data
        except ZabbixAPIException as e:
            logger.warning(f"{mt[425]}: {str(e)}")
            raise LookupError(f"{mt[425]}: '{item}'")  # failed to retrieve item error
        except Exception as e:
            logger.error(f"{str(e)}")
            raise ConnectionError(f"{mt[503]}")  # internal get item error

    def get_item_history(self, item_id, history=0, limit=25):
        try:
            item = self.zabbix.history.get(itemids=item_id, history=history, limit=limit, sortfield="clock",
                                           sortorder="DESC")
            if not item:
                logger.info(f"{mt[426]}: item:{item_id}")
                raise ValueError(f"{mt[426]} : {item_id}")  # there is no history error
            return item
        except ZabbixAPIException as e:
            logger.warning(f"{mt[427]}: {str(e)}")
            raise LookupError(f"{mt[427]}")  # failed to get history error
        except Exception as e:
            logger.error(f"{str(e)}")
            raise ConnectionError(f"{mt[504]}")  # internal get item history error

    def logout(self):
        try:
            self.zabbix.logout()
        except ZabbixAPIException as e:
            logger.error(f'{str(e)}')
            raise ConnectionError(f"{mt[505]}")  # internal logout error


class ZabbixHelper:
    def __init__(self):
        try:
            self.zabbix = ZabbixPackage(ZABBIX_URL)
            self.zabbix.login(ZABBIX_USER, ZABBIX_PASSWORD)
            self.host_id = self.zabbix.get_host_id(ZABBIX_HOST_NAME)
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
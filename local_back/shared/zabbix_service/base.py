from abc import ABC, abstractmethod


class ZabbixAPIBase(ABC):
    @abstractmethod
    def __init__(self, url):
        self.url = url
        self.zabbix = None
        self.host = None

        raise NotImplementedError

    @abstractmethod
    def login(self, username, password):
        raise NotImplementedError

    @abstractmethod
    def get_host_id(self, host_name):
        raise NotImplementedError

    @abstractmethod
    def get_item(self, host_id, item):
        raise NotImplementedError

    @abstractmethod
    def get_item_history(self, item_id):
        raise NotImplementedError

    @abstractmethod
    def logout(self):
        raise NotImplementedError

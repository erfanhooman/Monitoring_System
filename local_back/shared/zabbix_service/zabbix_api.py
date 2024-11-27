from base import ZabbixAPIBase
import json
import requests


class ZabbixBuiltinAPI(ZabbixAPIBase):  # TODO: Error Handling
    def __init__(self, url): #TODO: Test its
        super().__init__(url)
        self.token = None
        self.headers = {"Content-Type": "application/json-rpc"}

    def login(self, username, password):
        payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": username,
                "password": password
            },
            "id": 1,
            "auth": None
        }
        response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        self.auth_token = response.json().get('result')

    def get_host_id(self, host_name):
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
        return response.json().get('result')[0]['hostid']

    def get_item(self, host_id, item):
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
        return response.json().get('result')

    def get_item_history(self, item_id):
        payload = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 0,
                "itemids": item_id,
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": 10
            },
            "id": 4,
            "auth": self.auth_token
        }
        response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        return response.json().get('result')

    def logout(self):
        self.token = None

# from pyzabbix import ZabbixAPI
#
# # Connect to Zabbix server
# zabbix = ZabbixAPI("http://localhost/zabbix")
# zabbix.login("Admin", "zabbix")  # Replace with your credentials
#
# # Get host information
# host = zabbix.host.get(filter={"host": "Zabbix server"})
# print(host)
# print("Host ID:", host[0]['hostid'])
#
# items = zabbix.item.get(hostids=[host[0]['hostid']])
# for item in items:
#     print(f"Item Key: {item['key_']}, Name: {item['name']}")
#
# # Fetch CPU load
# cpu_item = zabbix.item.get(hostids=host[0]['hostid'], filter={"key_": "vfs.dev.queue_size"})
# print("Item:", cpu_item)
# discovery = zabbix.discover.get({
#     "output": "extend",
#     "hostids": host[0]['hostid'],
#     "filter": {"key_": "vfs.dev.discovery"}
# })
#
# item_prototypes = zabbix.itemprototype.get({
#     "output": "extend",
#     "hostids": host[0]['hostid'],
#     "search": {"key_": "vfs.dev.discovery"},  # Look for specific discovery items
# })
# print(item_prototypes)
#
#
# # Fetch history data for CPU load
# history = zabbix.history.get(itemids=cpu_item[0]['itemid'], history=0, limit=3, sortfield="clock", sortorder="DESC")
# print("History:", history)
#
# # Logout
# zabbix.user.logout()

from pyzabbix import ZabbixAPI

# Connect to Zabbix server
zabbix = ZabbixAPI("http://localhost/zabbix")
zabbix.login("Admin", "zabbix")  # Replace with your credentials

# Get host information
host = zabbix.host.get(filter={"host": "Zabbix server"})
# print(host)
# print("Host ID:", host[0]['hostid'])

items = zabbix.item.get(hostids=[host[0]['hostid']])
for item in items:
    print(f"Item Key: {item['key_']}, Name: {item['name']}")

# Fetch CPU load
cpu_item = zabbix.item.get(hostids=host[0]['hostid'], filter={"key_": "system.cpu.load[all,avg15]"})
# print("CPU Item:", cpu_item)

# Fetch history data for CPU load
history = zabbix.history.get(itemids=cpu_item[0]['itemid'], history=0, limit=3, sortfield="clock", sortorder="DESC")
print("CPU History:", history)

# Logout
zabbix.user.logout()
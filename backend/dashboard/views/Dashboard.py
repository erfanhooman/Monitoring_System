"""
you don't find what you looking for,
    when you're looking
"""

from rest_framework.views import APIView
from backend.services.zabbix_service.zabbix_packages import ZabbixHelper
from backend.utils import create_response
from backend.messages import mt


class DashboardView(APIView):
    def get(self, request):
        try:
            zabbix_helper = ZabbixHelper()

            # Fetch General Metric
            cpu = zabbix_helper.get_item_data('system.cpu.load[all,avg15]')
            ram = zabbix_helper.get_item_data('vm.memory.size[available]')
            disk = zabbix_helper.get_item_data('vfs.fs.size[/,total]')
            network = zabbix_helper.get_item_data('net.if.in["nekoray-tun"]')

            data = {
                'CPU': cpu,
                'RAM': ram,
                'Disk': disk,
                'Network': network
            }
            return create_response(success=True, data=data, message=mt[200])
        except ValueError as e:
            return create_response(success=False, message=str(e))


class RAMDetailView(APIView):
    def get(self, request):
        try:
            zabbix_helper = ZabbixHelper()

            ram = zabbix_helper.get_item_data('vm.memory.size[available]')
            # fetch the rest of detail ...

            data = {
                'RAM': ram,
                # ...
            }
            return create_response(success=True, data=data, message=mt[200])
        except ValueError as e:
            return create_response(success=False, message=str(e))


class CPUDetailView(APIView):
    def get(self, request):
        try:
            zabbix_helper = ZabbixHelper()

            cpu = zabbix_helper.get_item_data('system.cpu.load[all,avg15]')

            data = {
                'CPU load': cpu,
                # ...
            }
            return create_response(success=True, data=data, message=mt[200])
        except ValueError as e:
            return create_response(success=False, message=str(e))

"""
Remember one thing,
    Through every Dark night,
        There's a Bright Day After That,
            So no Matter how hard it get
                Stick your Chest Out, Keep your head Up
                    AND HANDLE IT.
"""

from django.db import models
from django.contrib.auth.models import User


class UserSystem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zabbix_server_url = models.CharField(max_length=255, default='localhost')
    zabbix_username = models.CharField(max_length=255, default='Admin')
    zabbix_password = models.CharField(max_length=255, default='zabbix')
    zabbix_host_name = models.CharField(max_length=255, default='Zabbix server')

    def __str__(self):
        return str(self.user)

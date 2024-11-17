"""
Remember one thing,
    Through every Dark night,
        There's a Bright Day After That,
            So no Matter how hard it get
                Stick your Chest Out, Keep your head Up
                    AND HANDLE IT.
"""

from django.contrib.auth.models import User
from django.db import models


class UserType(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'User'


class UserSystem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usersystem')
    zabbix_server_url = models.CharField(max_length=255, null=True, blank=True)
    zabbix_username = models.CharField(max_length=255, null=True, blank=True)
    zabbix_password = models.CharField(max_length=255, null=True, blank=True)
    zabbix_host_name = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.USER
    )
    admin = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subusers')

    @property
    def is_detail_available(self):
        return all([self.zabbix_server_url, self.zabbix_username, self.zabbix_password, self.zabbix_host_name])

    @property
    def zabbix_details(self):
        return {
            'url': self.zabbix_server_url,
            'username': self.zabbix_username,
            'password': self.zabbix_password,
            'host_name': self.zabbix_host_name
        }

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

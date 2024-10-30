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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zabbix_server_url = models.CharField(max_length=255)
    zabbix_username = models.CharField(max_length=255)
    zabbix_password = models.CharField(max_length=255)
    zabbix_host_name = models.CharField(max_length=255)
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.USER
    )
    admin = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,  # TODO: make sure of this
        null=True,
        blank=True,
        related_name='created_users'
    )

    def __str__(self):
        return f"{self.user.username}'s System"

    @property
    def zabbix_details(self):
        if self.user_type == UserType.USER:
            return {
                'url': self.admin.zabbix_server_url,
                'username': self.admin.zabbix_username,
                'password': self.admin.zabbix_password,
                'host_name': self.admin.zabbix_host_name
            }
        return {
            'url': self.zabbix_server_url,
            'username': self.zabbix_username,
            'password': self.zabbix_password,
            'host_name': self.zabbix_host_name
        }


class APIEndpoint(models.Model):
    Methods = (
        (0, 'GET'),
        (1, 'POST'),
    )
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    method = models.SmallIntegerField(choices=Methods)

    def __str__(self):
        return self.name


class UserPermission(models.Model):
    user = models.ForeignKey(UserSystem, on_delete=models.CASCADE, related_name='permissions')
    endpoint = models.ForeignKey(APIEndpoint, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'endpoint')

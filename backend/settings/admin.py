from django.contrib import admin

from .models import UserSystem, APIEndpoint, UserPermission

admin.site.register(UserSystem)
admin.site.register(APIEndpoint)
admin.site.register(UserPermission)

from django.contrib import admin

from .models import UserSystem, Permissions

admin.site.register(UserSystem)
admin.site.register(Permissions)

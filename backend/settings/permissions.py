"""
    Maybe the Journey isn't about becoming anything.

    Maybe its about unbecomming everything that isn't really you,
        so that can be who you were meant to be in the first place.

    -Paulo Caelho
"""

from rest_framework import permissions

from .models import UserType, UserPermission


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_superuser
        except:
            return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.usersystem.user_type == UserType.ADMIN
        except:
            return False


class HasViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user_system = request.user.usersystem
            if user_system.user_type == UserType.ADMIN:
                return True

            return UserPermission.objects.filter(
                user=user_system,
                endpoint__path=request.path
            ).exists()
        except:
            return False

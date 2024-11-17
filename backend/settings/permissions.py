"""
    Maybe the Journey isn't about becoming anything.

    Maybe its about unbecomming everything that isn't really you,
        so that can be who you were meant to be in the first place.

    -Paulo Caelho
"""

from rest_framework import exceptions as ex
from rest_framework import permissions

from backend.messages import mt


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.usersystem.active:
            return True
        raise ex.AuthenticationFailed(mt[433])



class IsDetailAvailable(permissions.BasePermission):
    def has_permission(self, request, view):
        user_system = request.user.usersystem

        if not user_system.is_detail_available:
            raise ex.PermissionDenied(mt[432])
        return True

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_superuser
        except:
            return False

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        if request.user.usersystem.user_type == 'admin':
            return True
        else:
            raise ex.PermissionDenied(mt[432])

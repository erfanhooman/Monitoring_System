"""
    Maybe the Journey isn't about becoming anything.

    Maybe its about unbecomming everything that isn't really you,
        so that can be who you were meant to be in the first place.

    -Paulo Caelho
"""
from rest_framework import exceptions as ex
from rest_framework import permissions

from backend.messages import mt
from settings.models import UserType


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_superuser and request.user and request.user.is_authenticated and request.user.usersystem.active:
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


class HasPermissionForView(permissions.BasePermission):
    required_permission = None

    def has_permission(self, request, view):
        #TODO: bug/ access using the superadmin to this pages cause an error
        try:
            if request.user.usersystem.user_type == UserType.ADMIN:
                return True

            user_system = request.user.usersystem
            if not user_system.active:
                return False

            if self.required_permission is None:
                raise ValueError("HasPermissionForView requires 'required_permission' to be set.")
        except Exception as e:
            raise ValueError("Don't have permission to perform this action")
        return user_system.permissions.filter(codename=self.required_permission).exists()

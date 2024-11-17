"""
    we don't quit,
        we don't cower,
            we don't run,
                we endure and conquer.
"""
from django.urls import path

from .views.managementview import UpdateZabbixSettingsView, LoginUserView
from .views.superadminviews import (
    AdminManagementView, AdminSignup
)
from .views.adminviews import UserSignup

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('settings/update/', UpdateZabbixSettingsView.as_view(), name='update'),
    path('super-admin/signup-user/', AdminSignup.as_view(), name='superadmin-signup'),
    path('super-admin/admin-management/<int:user_id>/', AdminManagementView.as_view(), name='admin-management'),
    path('super-admin/admin-management/', AdminManagementView.as_view(), name='admin-management'),
    path('admin/user/signup/', UserSignup.as_view(), name='user-signup'),
]
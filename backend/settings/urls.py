"""
    we don't quit,
        we don't cower,
            we don't run,
                we endure and conquer.
"""
from django.urls import path

from .views.managementview import UpdateZabbixSettingsView, LoginUserView
from .views.superadminviews import (
    AdminManagementView, AdminSignupView
)
from .views.adminviews import UserSignup, UserManagementView, ModifyUserPermissionsView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('super-admin/admin-signup/', AdminSignupView.as_view(), name='admin-signup'),
    path('super-admin/admin-management/', AdminManagementView.as_view(), name='admin-management'),
    path('settings/update/', UpdateZabbixSettingsView.as_view(), name='update'),
    path('admin/user-signup/', UserSignup.as_view(), name='user-signup'),
    path('admin/user-management/', UserManagementView.as_view(), name='user-management'),
    path('admin/user-management/permission/', ModifyUserPermissionsView.as_view(), name='modify-subuser-permissions'),

]
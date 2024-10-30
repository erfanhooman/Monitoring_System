"""
    we don't quit,
        we don't cower,
            we don't run,
                we endure and conquer.
"""

from django.urls import path

from .views import (
    SignupView, LoginUserView, UpdateZabbixSettingsView,
    AdminManagementView, AdminUserManagement, SignupSubUserView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('update/', UpdateZabbixSettingsView.as_view(), name='update'),
    path('super-admin/admin-management/', AdminManagementView.as_view(), name='admin-management'),
    path('admin/subusers/', AdminUserManagement.as_view(), name='admin-subuser-management'),
    path('admin/subusers/signup/', SignupSubUserView.as_view(), name='signup-subuser'),
]
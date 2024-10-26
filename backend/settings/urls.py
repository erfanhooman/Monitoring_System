from django.urls import path

from .views import SignupView, LoginView, UpdateZabbixSettingsView

urlpatterns = [
    path('singup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('update/', UpdateZabbixSettingsView.as_view(), name='update'),
]

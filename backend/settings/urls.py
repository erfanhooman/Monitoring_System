from django.urls import path

from .views import SignupView, LoginUserView, UpdateZabbixSettingsView

urlpatterns = [
    path('singup/', SignupView.as_view(), name='signup'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('update/', UpdateZabbixSettingsView.as_view(), name='update'),
]

from django.urls import path
from .views import SignupView, LoginView

urlpatterns = [
    path('singup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]

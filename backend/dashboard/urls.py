from django.urls import path
from .views.Dashboard import DashboardView, RAMDetailView, CPUDetailView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('ram/', RAMDetailView.as_view(), name='ram_detail'),
    path('cpu/', CPUDetailView.as_view(), name='cpu_detail'),
]
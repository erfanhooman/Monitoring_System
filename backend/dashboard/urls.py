from django.urls import path
from .views import Dashboard as Views

urlpatterns = [
    path('', Views.DashboardView.as_view(), name='dashboard'),
    path('ram/', Views.RamDetailView.as_view(), name='ram_detail'),
    path('cpu/', Views.CPUDetailView.as_view(), name='cpu_detail'),
    path('fs/', Views.FileSystemDetailView.as_view(), name='filesystem_detail'),
    path('disk/', Views.DiskDetailView.as_view(), name='disk_detail'),
    path('network/', Views.NetworkInterfaceDetailView.as_view(), name='network_detail'),
    path('general/', Views.GeneralDetailView.as_view(), name='general_detail'),

]
from django.urls import path
from . import views as vw

urlpatterns = [
    path('internal/problemreport/', vw.ProblemReportView.as_view(), name='problem-report'),
    path('api/prefalert/', vw.AlertPreferenceView.as_view(), name='alert-preference'),
]
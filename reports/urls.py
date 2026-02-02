from django.urls import path
from . import views

urlpatterns = [
    path('academic_reports',views.academic_reports,name='academic_reports'),
    path('financial_reports',views.financial_reports,name='financial_reports'),
]

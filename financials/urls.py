from django.urls import path
from . import views
urlpatterns=[
    path('financial_permit',views.financial_permit,name='financial_permit'),
    path('financial_permits',views.financial_permits,name='financial_permits'),
    path('permit/delete/<int:permit_id>/', views.delete_permit, name='delete_permit'),
]
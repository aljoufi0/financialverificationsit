from django.urls import path
from . import views
urlpatterns=[
    path('student',views.students,name='student'),
]
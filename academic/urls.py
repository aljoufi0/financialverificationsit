from django.urls import path
from . import views

urlpatterns=[
    path('student/search/', views.student_search, name='student_search'),
    path('student/update/<int:academic_number>/', views.update_student, name='update_student'),
    path('add_student',views.add_student,name='add_student'),
    path('fingerprint_management/',views.fingerprint_management,name='fingerprint_management'),
    path('fingerprint/delete/<int:fp_id>/', views.delete_fingerprint, name='delete_fingerprint'),
    path('api/student-search/', views.student_search_api, name='student_search_api'),
]
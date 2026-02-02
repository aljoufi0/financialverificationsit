from django.contrib import admin
from .models import StudentFingerprint


# Register your models here.
# admin.site.register(StudentFingerprint)
@admin.register(StudentFingerprint)
class StudentFingerprintAdmin(admin.ModelAdmin):
    list_display=('student','fingerprint_template','finger_index','fingerprint_quality',) 
    search_fields=('student',)
    list_filter=('finger_index',)



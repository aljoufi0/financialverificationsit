from django.contrib import admin
from django.utils.html import format_html # ضروري لعرض الـ HTML (الصور)
from .models import Student, Specialization, Semester, College, Cohort, Level

# تسجيل الجداول البسيطة
admin.site.register(Semester)
admin.site.register(College)
admin.site.register(Cohort)
admin.site.register(Level)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # أضفنا 'display_photo' في بداية القائمة لتظهر الصورة
    list_display = ('display_photo', 'academic_number', 'student_name', 'specialization', 'level','cohort','gender','created_at','created_by',)
    search_fields = ('student_name', 'academic_number')
    list_filter = ('specialization', 'level', 'semester')
    list_per_page = 50

    # دالة عرض الصورة المصغرة في جدول الطلاب
    def display_photo(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />', obj.profile_picture.url)
        return "لا توجد صورة"
    
    display_photo.short_description = 'الصورة'

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('specialization_name', 'college')
    search_fields = ('specialization_name',)
    list_filter = ('college',)
    list_per_page = 50
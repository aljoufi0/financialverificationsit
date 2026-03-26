from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Student, Specialization, Semester, College, Level

# 1. إعداد مورد البيانات (Resource) كما هو
class StudentResource(resources.ModelResource):
    specialization = fields.Field(
        column_name='التخصص',
        attribute='specialization',
        widget=ForeignKeyWidget(Specialization, 'specialization_name'))
    
    level = fields.Field(
        column_name='المستوى',
        attribute='level',
        widget=ForeignKeyWidget(Level, 'level_name'))

    semester = fields.Field(
        column_name='الفصل الدراسي',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, 'semester_name'))

    class Meta:
        model = Student
        fields = ('academic_number', 'student_name', 'specialization', 'level', 'semester', 'gender', 'academic_status')
        export_order = fields
        import_id_fields = ('academic_number',)
        skip_unchanged = True
        report_skipped = True

# 2. تسجيل الجداول البسيطة
admin.site.register(Semester)
admin.site.register(College)
admin.site.register(Level)

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('specialization_name', 'college')
    search_fields = ('specialization_name',)
    list_filter = ('college',)

# 3. إعداد جدول الطلاب مع الأوامر الديناميكية
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    
    list_display = ('display_photo', 'academic_number', 'student_name', 'specialization', 'level', 'semester', 'academic_status')
    search_fields = ('student_name', 'academic_number')
    list_filter = ('specialization', 'level', 'semester', 'academic_status')
    list_per_page = 50

    # دالة لجلب الإجراءات ديناميكياً
    def get_actions(self, request):
        actions = super().get_actions(request)
        
        # إضافة إجراءات الترفيع للمستويات ديناميكياً
        for level in Level.objects.all():
            action_name = f'promote_to_level_{level.id}'
            action_func = self.create_promote_level_action(level)
            actions[action_name] = (action_func, action_name, f"🔼 ترفيع إلى: {level.level_name}")

        # إضافة إجراءات الترفيع للفصول ديناميكياً
        for semester in Semester.objects.all():
            action_name = f'promote_to_semester_{semester.id}'
            action_func = self.create_promote_semester_action(semester)
            actions[action_name] = (action_func, action_name, f"📅 نقل إلى: {semester.semester_name}")
            
        return actions

    # مصنع وظائف ترفيع المستويات
    def create_promote_level_action(self, level):
        def promote_to_level(modeladmin, request, queryset):
            updated = queryset.update(level=level)
            modeladmin.message_user(request, f"تم ترفيع {updated} طالب إلى {level.level_name} بنجاح.", messages.SUCCESS)
        promote_to_level.short_description = f"ترفيع إلى {level.level_name}"
        return promote_to_level

    # مصنع وظائف ترفيع الفصول
    def create_promote_semester_action(self, semester):
        def promote_to_semester(modeladmin, request, queryset):
            updated = queryset.update(semester=semester)
            modeladmin.message_user(request, f"تم نقل {updated} طالب إلى {semester.semester_name} بنجاح.", messages.SUCCESS)
        promote_to_semester.short_description = f"نقل إلى {semester.semester_name}"
        return promote_to_semester

    # عرض الصورة المصغرة
    def display_photo(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="48" style="border-radius: 5px; object-fit: cover;" />', obj.profile_picture.url)
        return "لا توجد صورة"
    
    display_photo.short_description = 'الصورة'  
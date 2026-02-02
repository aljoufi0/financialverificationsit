from django.contrib import admin
from .models import UniversitySettings, SliderImage
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UniversityBranch, UserProfile

# تخصيص ظهور إعدادات الجامعة
@admin.register(UniversitySettings)
class UniversitySettingsAdmin(admin.ModelAdmin):
    # عرض الحقول في القائمة الرئيسية
    list_display = ('name', 'phone', 'email')
    
    # منع إضافة أكثر من سجل واحد (اختياري)
    # لأن الموقع عادةً يحتاج إعدادات لجامعة واحدة فقط
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

# تخصيص ظهور صور السلايدر
@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    # عرض الصورة (مصغرة) والوصف وحالة التفعيل
    list_display = ('caption', 'is_active')
    # إمكانية التفعيل والتعطيل مباشرة من القائمة
    list_editable = ('is_active',)



# إضافة حقل الفرع داخل صفحة المستخدم
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'بيانات الفرع'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# إعادة تسجيل جدول المستخدمين
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# تسجيل جدول الفروع بشكل مستقل أيضاً
@admin.register(UniversityBranch)
class UniversityBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
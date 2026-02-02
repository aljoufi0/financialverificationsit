from django.db import models
from django.contrib.auth.models import User

# الموديل المسؤول عن اسم الجامعة وبيانات الفوتر
class UniversitySettings(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم الجامعة")
    address = models.CharField(max_length=500, verbose_name="العنوان")
    phone = models.CharField(max_length=50, verbose_name="رقم الهاتف")
    whatsapp = models.CharField(max_length=50, verbose_name="رقم الواتساب")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    copyright_text = models.CharField(max_length=255, verbose_name="حقوق النشر")
    logo = models.ImageField(upload_to='university/logos/', verbose_name="شعار الجامعة", blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name ="الجامعة"
        verbose_name_plural = "تفاصيل الجامعة"

# الموديل المسؤول عن صور السلايدر
class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/', verbose_name="الصورة")
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="وصف")
    is_active = models.BooleanField(default=True, verbose_name="تفعيل")
    
    

    def __str__(self):
    # نستخدم or لضمان إرجاع نص دائماً حتى لو كان الحقل فارغاً
        return self.caption or f"صورة سلايدر رقم {self.id}"

    
    class Meta:
        verbose_name = "سلايدر"
        verbose_name_plural = "صور السلايدرات"


# 1. جدول الفروع
class UniversityBranch(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم الفرع")
    address = models.CharField(max_length=500, verbose_name="العنوان", blank=True)
    phone = models.CharField(max_length=50, verbose_name="هاتف الفرع", blank=True)
    class Meta:
        verbose_name = "فرع الجامعة"
        verbose_name_plural = "فروع الجامعة"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    branch = models.ForeignKey(
        UniversityBranch, 
        on_delete=models.PROTECT, # حماية الفرع من الحذف إذا كان به موظفون
        related_name='employees',
        verbose_name="الفرع التابع له"
    )

    class Meta:
        verbose_name = "بروفايل الموظف"
        verbose_name_plural = "بروفايلات الموظفين"

    def __str__(self):
        return f"{self.user.username} - {self.branch.name}"
from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from django.conf import settings
from django.contrib.auth.models import User


class Level(models.Model):
    level_name = models.CharField(
        max_length=100, 
        verbose_name="اسم المستوى"
    )

    class Meta:
        verbose_name = "مستوى الدراسي"
        verbose_name_plural = "المستويات الدراسية"
        

    def __str__(self):
        return self.level_name
    

class Semester(models.Model):
    semester_name = models.CharField(
        max_length=255, 
        verbose_name="اسم الفصل"
    )

    class Meta:
        verbose_name = "الفصل دراسي"
        verbose_name_plural = "الفصول الدراسية"
        

    def __str__(self):
        return self.semester_name





    

class Specialization(models.Model):
    specialization_name = models.CharField(
        max_length=255, 
        verbose_name="اسم التخصص"
    )

    college = models.ForeignKey(
        'College', 
        on_delete=models.PROTECT, 
        verbose_name="الكلية التابع لها"
    )

    class Meta:
        verbose_name = "تخصص"
        verbose_name_plural = "التخصصات"
        

    def __str__(self):
        return self.specialization_name
    

class College(models.Model):
    college_name = models.CharField(
        max_length=255, 
        verbose_name="اسم الكلية"
    )

    class Meta:
        verbose_name = "كلية"
        verbose_name_plural = "الكليات"
        

    def __str__(self):
        return self.college_name
    

class Student(models.Model):

    ACADEMIC_STATUS_CHOICES = [
        ('active', 'نشط'),
        ('suspended', 'موقف'),
        ('graduated', 'خريج'),
    ]
    GENDER_CHOICES = [
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    ]

    academic_number = models.BigIntegerField(
        primary_key=True, 
        unique=True, 
        verbose_name="الرقم الأكاديمي"
    ) 


    student_name = models.CharField(
        max_length=255, 
        verbose_name="اسم الطالب"
    ) 


    # --- الحقل الجديد لتخزين صورة الباركود ---
    barcode_image = models.ImageField(
        upload_to='barcodes/%y/%m/%d',
        blank=True, 
        null=True,
        verbose_name="صورة الباركود"
    )





    specialization = models.ForeignKey(
        'Specialization', 
        on_delete=models.PROTECT, 
        verbose_name="معرف التخصص"
    ) 

    semester = models.ForeignKey(
        'Semester', 
        on_delete=models.PROTECT, 
        verbose_name="معرف الفصل"
    ) 


    level = models.ForeignKey(
        'Level', 
        on_delete=models.PROTECT, 
        verbose_name="المستوى الدراسي"
    ) 

    profile_picture = models.ImageField(upload_to='photos/%y/%m/%d',
        blank=True, 
        null=True,
        verbose_name="الصورة"
    ) 

    academic_status = models.CharField(
        max_length=10, 
        choices=ACADEMIC_STATUS_CHOICES, 
        verbose_name="الحالة الأكاديمية"
    ) 

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES, 
        default='male',      
        verbose_name="الجنس"
    )


    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name='تاريخ الاضافة')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='تم الانشاء بواسطة')


    class Meta:
        verbose_name = "طالب"
        verbose_name_plural = "الطلاب"
        permissions = [
            ("can_view_academic_reports", "يمكنه عرض التقارير الأكاديمية"),
            ("can_view_financial_reports", "يمكنه عرض التقارير المالية"),
        ]
    

    def __str__(self):
        return self.student_name
    # f"{self.academic_number} - {self.student_name}"



    # --- دالة الحفظ التلقائي لتوليد الباركود عند كل حفظ للطالب ---
    def save(self, *args, **kwargs):
        # نقوم بتوليد باركود جديد بناءً على الرقم الأكاديمي الحالي
        COD128 = barcode.get_barcode_class('code128')
        rv = BytesIO()
        code = COD128(str(self.academic_number), writer=ImageWriter())
        code.write(rv)
        
        filename = f'{self.academic_number}.png'
        # save=False تمنع الدخول في حلقة تكرار لا نهائية لدالة save
        self.barcode_image.save(filename, File(rv), save=False)
        
        super().save(*args, **kwargs)

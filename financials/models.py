from django.db import models
from students.models import Student
from django.contrib.auth.models import User
# Create your models here.


class Permit(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        verbose_name="الطالب"
    )
    start_date = models.DateField(
        auto_now_add=True, 
        verbose_name="تاريخ الإصدار"
    )
    end_date = models.DateField(
        verbose_name="تاريخ الانتهاء"
    )

    statement = models.TextField(
        null=True,
        blank=True,
        verbose_name="البيان"


    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="حالة التصريح"
    )


    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="المستخدم ",
        )

    class Meta:
        verbose_name = "تصريح"
        verbose_name_plural = "التصاريح"
    def __str__(self):
        return self.student.student_name
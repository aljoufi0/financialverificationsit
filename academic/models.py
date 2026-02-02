from django.db import models
from students.models import Student
from django.contrib.auth.models import User

class StudentFingerprint(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        verbose_name="الطالب"
    )
    fingerprint_template = models.TextField(
        verbose_name="بيانات البصمة الرقمية"
    )

    finger_index = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="رقم الإصبع"
    )

    fingerprint_quality = models.PositiveSmallIntegerField(
        verbose_name="جودة البصمة",
        help_text="درجة جودة البصمة من 1 إلى 100"
    )

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True,
        verbose_name="المستخدم ",
        )

    class Meta:
        verbose_name = "بصمة طالب"
        verbose_name_plural = "بصمات الطلاب"
        db_table = 'Student_Fingerprints'

    def __str__(self):
        return self.student.student_name


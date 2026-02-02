
from django.shortcuts import render
from django.db.models import Exists, OuterRef
from students.models import Student, Cohort, Specialization, Semester, Level
from academic.models import StudentFingerprint
from django.contrib.auth.decorators import login_required



@login_required
def academic_reports(request):
    context = {
        'cohorts': Cohort.objects.all(),
        'specializations': Specialization.objects.all(),
        'semesters': Semester.objects.all(),
        'levels': Level.objects.all(),
    }

    # التحقق من وجود بصمة للطالب في جدول StudentFingerprint
    students = Student.objects.annotate(
        has_fingerprint=Exists(
            StudentFingerprint.objects.filter(student_id=OuterRef('pk'))
        )
    )

    # تطبيق الفلاتر
    c_id = request.GET.get('cohort')
    s_id = request.GET.get('specialization')
    sem_id = request.GET.get('semester')
    l_id = request.GET.get('level')

    if c_id: students = students.filter(cohort_id=c_id)
    if s_id: students = students.filter(specialization_id=s_id)
    if sem_id: students = students.filter(semester_id=sem_id)
    if l_id: students = students.filter(level_id=l_id)

    context['students'] = students
    return render(request, 'reports/academic_reports.html', context)
@login_required
def financial_reports(request):
    return render(request,'reports/financial_reports.html')

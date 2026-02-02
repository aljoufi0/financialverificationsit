from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from students.models import Student, Cohort, Specialization, Semester, Level, College
from .models import Permit
from pages.models import UniversitySettings
from django.utils import timezone
from datetime import timedelta
from django.db.models import OuterRef, Subquery 
from django.contrib.auth.decorators import login_required

# 1. إصدار تصريح لطالب
@login_required
def financial_permit(request):
    # تحقق يدوي من الصلاحية مع إرسال رسالة
    if not (request.user.has_perm('financials.add_permit')):
        messages.error(request, "⚠️ تنبية: ليس لديك صلاحية في الشؤون المالية    .")
        return redirect('index')

    student = None
    query = request.GET.get('search_query')
    college = UniversitySettings.objects.first()

    if query:
        if query.isdigit():
            student = Student.objects.filter(academic_number=query).first()
        else:
            student = Student.objects.filter(student_name__icontains=query).first()
        
        if not student:
            messages.error(request, f"⚠️ لم يتم العثور على طالب بالبيانات: ({query})")

    if request.method == 'POST':
        academic_number = request.POST.get('academic_number')
        target_student = get_object_or_404(Student, academic_number=academic_number)
        
        try:
            Permit.objects.create(
                student=target_student,
                end_date=request.POST.get('end_date'),
                statement=request.POST.get('statement'),
                is_active=True
            )
            messages.success(request, f"✅ تم إصدار التصريح بنجاح للطالب: {target_student.student_name}")
            return redirect('financial_permit')
        except Exception as e:
            messages.error(request, f"❌ حدث خطأ أثناء حفظ التصريح: {e}")

    return render(request, 'financials/financial_permit.html', {'student': student,'college': college,})

# 2. حذف تصريح
@login_required
def delete_permit(request, permit_id):
    # تحقق يدوي من صلاحية الحذف
    if not request.user.has_perm('financials.delete_permit'):
        messages.error(request, "🚫 لا تملك صلاحية حذف التصاريح المالية.")
        return redirect('index')

    permit = get_object_or_404(Permit, id=permit_id)
    student_name = permit.student.student_name
    academic_num = permit.student.academic_number
    permit.delete()
    messages.success(request, f"🗑️ تم حذف التصريح الخاص بالطالب {student_name} بنجاح.")
    return redirect(reverse('financial_permit') + f'?search_query={academic_num}')

# 3. إصدار تصاريح عامة/جماعية
@login_required
def financial_permits(request):
    # تحقق يدوي من صلاحية الإضافة
    if not (request.user.has_perm('financials.add_permit')):
        messages.error(request, "⚠️ تنبية: ليس لديك صلاحية في الشؤون المالية    .")
        return redirect('index')

    college = UniversitySettings.objects.first()
    context = {
        'cohorts': Cohort.objects.all(),
        'specializations': Specialization.objects.all(),
        'semesters': Semester.objects.all(),
        'levels': Level.objects.all(),
        'colleges': College.objects.all(),
        'college': college,
    }

    students = Student.objects.all()
    c_id = request.GET.get('cohort')
    s_id = request.GET.get('specialization')
    sem_id = request.GET.get('semester')
    l_id = request.GET.get('level')
    col_id = request.GET.get('college')
    filter_date = request.GET.get('filter_date')

    if c_id: students = students.filter(cohort_id=c_id)
    if s_id: students = students.filter(specialization_id=s_id)
    if sem_id: students = students.filter(semester_id=sem_id)
    if l_id: students = students.filter(level_id=l_id)
    if col_id: students = students.filter(specialization__college_id=col_id)

    if filter_date:
        latest_permit_date = Permit.objects.filter(
            student=OuterRef('pk')
        ).order_by('-end_date').values('end_date')[:1]

        students = students.annotate(
            current_permit_end=Subquery(latest_permit_date)
        ).filter(current_permit_end__lte=filter_date)

    context['students'] = students

    if request.method == 'POST':
        selected_academic_numbers = request.POST.getlist('selected_students')
        end_date = request.POST.get('end_date')
        statement = request.POST.get('statement')

        if not selected_academic_numbers:
            messages.error(request, "⚠️ يرجى اختيار طالب واحد على الأقل.")
        elif not end_date:
            messages.error(request, "⚠️ يرجى تحديد تاريخ الانتهاء.")
        else:
            for acc_num in selected_academic_numbers:
                Permit.objects.create(
                    student_id=acc_num,
                    end_date=end_date,
                    statement=statement,
                    is_active=True
                )
            messages.success(request, f"✅ تم إصدار {len(selected_academic_numbers)} تصريح بنجاح.")
            return redirect('financial_permits')

    return render(request, 'financials/financial_permits.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from students.models import Student, Specialization, Cohort, Level, Semester, College
from pages.models import UniversitySettings
from .models import StudentFingerprint
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# 1. دالة البحث عن الطلاب (صلاحية العرض)
@login_required
def student_search(request):
    # السماح بالدخول لمن يملك صلاحية العرض
    if not request.user.has_perm('students.view_student'):
        messages.error(request, "⚠️ ليس لديك صلاحية للبحث عن الطلاب أو عرض بياناتهم.")
        return redirect('index')

    college = UniversitySettings.objects.first()
    student = None
    query = request.GET.get('search_query')

    if query:
        if query.isdigit():
            student = Student.objects.filter(academic_number=query).first()
        else:
            student = Student.objects.filter(student_name__icontains=query).first()
        
        if query and not student:
            messages.warning(request, f"🔍 لم يتم العثور على طالب بالبيانات: ({query})")

    context = {
        'student': student,
        'specializations': Specialization.objects.all(),
        'cohorts': Cohort.objects.all(),
        'levels': Level.objects.all(),
        'semesters': Semester.objects.all(),
        'college': college,
    }
    return render(request, 'academic/student_search.html', context)

# 2. دالة التحديث (تمنع الحفظ فقط وتسمح بالدخول للعرض إذا كان في نفس صفحة البحث)
@login_required
def update_student(request, academic_number):
    if not request.user.has_perm('students.change_student'):
        messages.error(request, "🚫 نعتذر، لا تملك الصلاحية لتعديل بيانات الطلاب.")
        return redirect('index')

    if request.method == 'POST':
        student = get_object_or_404(Student, academic_number=academic_number)
        try:
            student.student_name = request.POST.get('student_name')
            student.specialization_id = request.POST.get('specialization')
            student.cohort_id = request.POST.get('cohort')
            student.level_id = request.POST.get('level')
            student.semester_id = request.POST.get('semester')
            student.academic_status = request.POST.get('academic_status')
            student.gender = request.POST.get('gender')
            if request.FILES.get('profile_picture'):
                student.profile_picture = request.FILES.get('profile_picture')
                
            student.save()
            messages.success(request, f"✅ تم تحديث بيانات الطالب {student.student_name} بنجاح.")
        except Exception as e:
            messages.error(request, f"❌ خطأ في التحديث: {e}")
            
    return redirect(f'/academic/student/search/?search_query={academic_number}')

# 3. دالة الإضافة (صلاحية الإضافة)
@login_required
def add_student(request):
    if not request.user.has_perm('students.add_student'):
        messages.error(request, "⚠️ تنبيه: ليس لديك صلاحية لتسجيل طلاب جدد.")
        return redirect('index')

    college = UniversitySettings.objects.first()
    if request.method == 'POST':
        try:
            Student.objects.create(
                academic_number=request.POST.get('academic_number'),
                student_name=request.POST.get('student_name'),
                specialization_id=request.POST.get('specialization'),
                cohort_id=request.POST.get('cohort'),
                level_id=request.POST.get('level'),
                semester_id=request.POST.get('semester'),
                academic_status=request.POST.get('academic_status'),
                gender=request.POST.get('gender'),
                profile_picture=request.FILES.get('profile_picture'),
                created_by=request.user
            )
            messages.success(request, '✅ تم إضافة الطالب بنجاح إلى النظام.')
        except Exception as e:
            messages.error(request, f'❌ حدث خطأ: {e}')
        
    context = {
        'specializations': Specialization.objects.all(),
        'cohorts': Cohort.objects.all(),
        'levels': Level.objects.all(),
        'semesters': Semester.objects.all(),
        'college': college,
    }
    return render(request, 'academic/add_student.html', context)

# 4. إدارة البصمة (تسمح بالدخول للعرض للجميع، وتمنع الحفظ لغير المصرح لهم)
@login_required
def fingerprint_management(request):
    # # السماح بالدخول لجميع الموظفين الذين لديهم صلاحية عرض الطلاب
    # if not request.user.has_perm('students.view_student'):
    #     messages.error(request, "🔒 قسم إدارة البصمة محظور لغير المصرح لهم.")
    #     return redirect('index')

    college = UniversitySettings.objects.first()
    student = None
    query = request.GET.get('search_query')

    if query:
        if query.isdigit():
            student = Student.objects.filter(academic_number=query).first()
        else:
            student = Student.objects.filter(student_name__icontains=query).first()
        
        if not student:
            messages.error(request, f"❌ عذراً، لم يتم العثور على أي طالب بالبيانات: ({query})")

    # حماية "عملية الحفظ" فقط
    if request.method == 'POST':
        if not request.user.has_perm('students.add_student'):
            messages.error(request, "🚫 نعتذر، لا تملك صلاحية ربط بصمات جديدة.")
            return redirect('fingerprint_management')

        academic_number = request.POST.get('academic_number')
        try:
            target_student = get_object_or_404(Student, academic_number=academic_number)
            StudentFingerprint.objects.create(
                student=target_student,
                fingerprint_template=request.POST.get('fingerprint_id'),
                finger_index=request.POST.get('finger_index'),
                fingerprint_quality=request.POST.get('fingerprint_quality', 100)
            )
            messages.success(request, f"✅ تم ربط البصمة بنجاح للطالب « {target_student.student_name} »")
        except Exception as e:
            messages.error(request, f"❌ حدث خطأ أثناء الربط: {e}")

        return redirect('fingerprint_management')

    return render(request, 'academic/fingerprint_management.html', {'student': student,'college': college,})

# 5. حذف البصمة (منع الحذف فقط)
@login_required
def delete_fingerprint(request, fp_id):
    # التحقق من صلاحية التعديل لتنفيذ الحذف
    if not request.user.has_perm('students.delete_student'):
        messages.error(request, "🚫 لا تملك صلاحية حذف روابط البصمات.")
        return redirect('fingerprint_management')

    fingerprint = get_object_or_404(StudentFingerprint, id=fp_id)
    student_name = fingerprint.student.student_name
    academic_num = fingerprint.student.academic_number
    fingerprint.delete()
    messages.success(request, f"🗑️ تم حذف ربط البصمة للطالب {student_name} بنجاح.")
    return redirect(reverse('fingerprint_management') + f'?search_query={academic_num}')

# 6. API البحث
@login_required
def student_search_api(request):
    if not request.user.has_perm('students.view_student'):
        return JsonResponse({'results': [], 'error': 'No permission'}, status=403)
    
    query = request.GET.get('q', '')
    results = []
    if query:
        students = Student.objects.filter(student_name__icontains=query)[:20]
        for s in students:
            results.append({
                'id': s.academic_number,
                'text': f"{s.student_name} ({s.academic_number})"
            })
    return JsonResponse({'results': results})
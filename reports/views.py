
from django.shortcuts import render
from django.db.models import Exists, OuterRef
from students.models import Student, Specialization, Semester, Level
from academic.models import StudentFingerprint
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Q
from students.models import  Specialization, Level, Semester


@login_required
def academic_reports(request):
    # الحارس: لا يدخل إلا من لديه صلاحية عرض الطلاب
    if not request.user.has_perm('students.can_view_academic_reports'):
        messages.error(request, "🛑 عذراً، ليس لديك صلاحية الوصول للتقارير الأكاديمية.")
        return redirect('index')

    context = {
        'specializations': Specialization.objects.all(),
        'semesters': Semester.objects.all(),
        'levels': Level.objects.all(),
    }

    # التحقق من وجود بصمة للطالب
    students = Student.objects.annotate(
        has_fingerprint=Exists(
            StudentFingerprint.objects.filter(student_id=OuterRef('pk'))
        )
    )

    # تطبيق الفلاتر (كما هي في كودك)
    s_id = request.GET.get('specialization')
    sem_id = request.GET.get('semester')
    l_id = request.GET.get('level')

    
    if s_id: students = students.filter(specialization_id=s_id)
    if sem_id: students = students.filter(semester_id=sem_id)
    if l_id: students = students.filter(level_id=l_id)

    context['students'] = students
    return render(request, 'reports/academic_reports.html', context)

@login_required





def financial_reports(request):
    # الحارس: يمكننا ربطها بصلاحية مالية أو صلاحية العرض العام 
    # سنفترض وجود تطبيق اسمه 'finance' أو نستخدم صلاحية مخصصة
    if not request.user.has_perm('students.can_view_financial_reports'): # أو أي صلاحية تراها مناسبة للمالية
        messages.error(request, "💰 عذراً، قسم التقارير المالية محظور لغير المصرح لهم.")
        return redirect('index')
        
    # 1. جلب تاريخ اليوم للمقارنة مع تاريخ انتهاء التصريح
    today = timezone.now().date()

    # 2. جلب قيم الفلترة من الرابط (URL Parameters)
    search_query = request.GET.get('search_name', '').strip()
    spec_id = request.GET.get('specialization', '')
    level_id = request.GET.get('level', '')
    semester_id = request.GET.get('semester', '')
    permit_status = request.GET.get('permit_status', 'all')

    # 3. البداية بجميع الطلاب مع تحسين الأداء بجلب العلاقات
    students = Student.objects.select_related('specialization', 'level', 'semester').all()

    # 4. تطبيق فلترة البحث (الاسم أو الرقم الأكاديمي)
    if search_query:
        students = students.filter(
            Q(student_name__icontains=search_query) | 
            Q(academic_number__icontains=search_query)
        )
    
    # 5. فلترة التخصص والمستوى والفصل
    if spec_id:
        students = students.filter(specialization_id=spec_id)
    
    if level_id:
        students = students.filter(level_id=level_id)
        
    if semester_id:
        students = students.filter(semester_id=semester_id)

    # 6. منطق فلترة "حالة التصريح" المطور (بناءً على التاريخ والحجوزات)
    if permit_status == 'active':
        # فعال: التصريح نشط يدوياً وتاريخ الانتهاء لم يأتِ بعد
        students = students.filter(
            permit__is_active=True, 
            permit__end_date__gte=today
        ).distinct()

    elif permit_status == 'expired':
        # منتهي: إما تاريخه قديم أو تم إيقافه يدوياً
        students = students.filter(
            Q(permit__end_date__lt=today) | 
            Q(permit__is_active=False)
        ).distinct()

    elif permit_status == 'no_permit':
        # بدون تصريح: الطلاب الذين لا يملكون أي سجل في جدول التصاريح نهائياً
        students = students.filter(permit__isnull=True)

    # 7. تجهيز البيانات للقوائم المنسدلة والسياق
    context = {
        'students': students,
        'specializations': Specialization.objects.all(),
        'levels': Level.objects.all(),
        'semesters': Semester.objects.all(),
        'today': today,  # نرسله للقالب لتلوين الحالات برمجياً
    }
    
    return render(request, 'reports/financial_reports.html', context)
from django.shortcuts import render
from .models import Student
from financials.models import Permit
from django.utils import timezone
from pages.models import UniversitySettings 
from django.contrib.auth.decorators import login_required




def students(request):
    college = UniversitySettings.objects.first()
    query = request.GET.get('academic_query', '').strip()
    student = None
    permit_valid = False
    latest_permit = None
    all_permits = []
    error_message = None # متغير جديد لحمل رسالة الخطأ

    if query:
        # فحص: هل النص المدخل عبارة عن أرقام فقط؟
        if query.isdigit():
            # إذا كان أرقاماً، نبحث كالمعتاد
            student = Student.objects.filter(academic_number=query).select_related(
                'specialization', 'level', 'semester', 'cohort'
            ).first()
            
            if student:
                today = timezone.now().date()
                all_permits = student.permit_set.all().order_by('-end_date')[:2]
                
                for p in all_permits:
                    delta = p.end_date - today
                    p.days_left = delta.days if delta.days > 0 else 0

                latest_permit = all_permits.first()
                if latest_permit and latest_permit.end_date >= today and latest_permit.is_active:
                    permit_valid = True
            else:
                # إذا كان الرقم غير موجود في قاعدة البيانات
                error_message = f"عذراً، لا يوجد طالب مسجل بالرقم الأكاديمي: {query}"
        else:
            # إذا قام المستخدم بإدخال حروف (هذا هو طلبك الأساسي)
            error_message = "⚠️ تنبيه: يرجى إدخال أرقام فقط في خانة البحث (الرقم الأكاديمي لا يحتوي على حروف)."

    context = {
        'student': student,
        'query': query,
        'permit_valid': permit_valid,
        'latest_permit': latest_permit,
        'all_permits': all_permits, 
        'college': college,
        'error_message': error_message, # نمرر الرسالة للقالب
    }
    return render(request, 'students/student.html', context)
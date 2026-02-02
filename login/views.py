from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from pages.models import UniversitySettings

def login_view(request):
    # إذا كان المستخدم مسجل دخول بالفعل، وجهه فوراً لصفحة البحث
    if request.user.is_authenticated:
        return redirect('/')

    college = UniversitySettings.objects.first()
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() # جلب المستخدم مباشرة من الفورم المحقق
            auth_login(request, user)
            return redirect('/') 
        # ملاحظة: إذا لم يكن صالحاً، سيستمر الكود للأسفل ويعيد عرض الفورم مع الأخطاء
    else:
        form = AuthenticationForm()

    context = {
        'college': college,
        'form': form
    }
    return render(request, 'login/login.html', context)
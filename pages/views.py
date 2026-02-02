from django.shortcuts import render
from .models import UniversitySettings, SliderImage

def index(request):
    
    college = UniversitySettings.objects.first()
    
    # جلب جميع صور السلايدر المفعلة
    slides = SliderImage.objects.filter(is_active=True)
    
    context = {
        'college': college,
        'slides': slides,
    }
    
    return render(request, 'pages/index.html', context)
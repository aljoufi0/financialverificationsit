from django.contrib import admin
from .models import Permit


# Register your models here.
# admin.site.register(Permit)
@admin.register(Permit)
class PermitAdmin(admin.ModelAdmin):
    list_display=('student','end_date','statement','is_active',)
    search_fields=('student',)
    list_filter=('is_active','end_date',)

from django.contrib import admin
from .models import Job

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "location", "employment_type", "is_active", "created_at")
    list_filter = ("employment_type", "is_active", "created_at")
    search_fields = ("title", "description", "requirements")

admin.site.register(Job,JobAdmin)
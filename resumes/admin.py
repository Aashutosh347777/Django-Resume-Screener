from django.contrib import admin
from .models import Resumes
# Register your models here.
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate_name','job','email','ats_score','uploaded_at')
    search_fields = ('candidate_name','emial','skill')
    list_filter = ('job','uploaded_at')

admin.site.register(Resumes,ResumeAdmin)
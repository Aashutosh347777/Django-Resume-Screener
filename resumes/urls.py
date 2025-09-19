from django.urls import path
from.import views as res_views
app_name = 'resumes'

urlpatterns = [
    path('resumes_list/', res_views.reseumes_list, name = 'resumes_list'),
    path('flagged_resumes/', res_views.flagged_resumes, name = 'flagged_resumes'),
    path('rescreen_resume/<int:resume_id>/', res_views.rescreen_resume, name = 'rescreen_resume'),
]
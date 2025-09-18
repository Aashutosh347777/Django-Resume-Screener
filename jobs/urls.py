from django.urls import path
from . import views as job_veiws
app_name = 'jobs'

urlpatterns = [
    path('post_job/',job_veiws.post_job, name = 'post_job'),
    path('upload_resume/', job_veiws.upload_resume, name = 'upload_resume'),
    path('job_details/<int:job_id>/', job_veiws.job_details, name = 'job_details'),
    path('resume_details/<int:resume_id>/', job_veiws.resume_detials, name = 'resume_details'),
    path('close_posting/<int:job_id>/', job_veiws.close_posting, name = 'close_posting'),
]
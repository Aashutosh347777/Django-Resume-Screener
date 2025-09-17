from django.urls import path
from . import views as job_veiws
app_name = 'jobs'

urlpatterns = [
    path('post_job/',job_veiws.post_job, name = 'post_job'),
    path('upload_resume/', job_veiws.upload_resume, name = 'upload_resume'),
]
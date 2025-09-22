from django.urls import path
from . import views as job_veiws
app_name = 'jobs'

urlpatterns = [
    path('post_job/',job_veiws.post_job, name = 'post_job'),
    path('job_details/<int:job_id>/', job_veiws.job_details, name = 'job_details'),
    path('close_posting/<int:job_id>/', job_veiws.close_posting, name = 'close_posting'),
    path('jobs_list/', job_veiws.jobs_list, name = 'jobs_list'),
    path('screening_list/', job_veiws.screening_list, name = 'screening_jobs_list'),
    path('top_candidates/<int:job_id>/', job_veiws.top_candidates_list, name='top_candidates_list'),
    
]
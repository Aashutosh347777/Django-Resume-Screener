from django.urls import path
from.import views as res_views
app_name = 'resumes'

urlpatterns = [
    path('resumes_list/', res_views.reseumes_list, name = 'resumes_list'),
]
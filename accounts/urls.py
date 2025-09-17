from django.urls import path
from accounts import views as acc_views
from django.contrib.auth import views as auth_views
app_name = 'accounts'

urlpatterns = [
    path('dashboard/',acc_views.dashboard, name = 'dashboard'),
    path('dashboard/',acc_views.dashboard, name = 'dashboard'),
    path('random/',acc_views.random, name = 'random'),
]
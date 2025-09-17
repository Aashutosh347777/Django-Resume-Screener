from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.contrib import messages
from jobs.models import Job
from resumes.models import Resumes

# Create your views here.

@login_required
def dashboard(request):
    user_role = request.user.role
    context = {}

    if user_role == 'hr':
        #  filters jobs by the specific hr
        jobs = Job.objects.filter(created_by=request.user).order_by('-created_at')
        context['jobs'] = jobs

    elif user_role == 'recruiter':
        # get the resumes uploaded
        resumes = Resumes.objects.all().order_by('-uploaded_at')
        context['resumes'] = resumes

    return render(request, "accounts/dashboard.html",context)

def random(request):
    return render(request, "accounts/random.html")

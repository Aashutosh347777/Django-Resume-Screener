from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job
from resumes.models import Resumes
from django.contrib import messages
import PyPDF2
from docx import Document
import io
import requests
import re
import os
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from django.http import FileResponse,Http404

# Create your views here.
@login_required
def post_job(request):
    # verify if user is hr or not
    if request.user.role != 'hr':
        return redirect('accounts:dashboard')
    
    form = JobForm(request.POST)
    if request.method == "POST":
        # collect form
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            return redirect('accounts:dashboard')
        else:
            form = JobForm()

    context ={
        'form': form
    }
    return render(request, "jobs/post_jobs.html", context)



@login_required
def job_details(request, job_id):
    #getting the job id for the sepeicfic job
    job = get_object_or_404(Job, id = job_id)

    # resumes linked to the jobs
    resumes = Resumes.objects.filter(job = job).order_by('-match_score')

    context = {
        'job' : job,
        'resumes' : resumes
    }

    return render(request, 'jobs/job_details.html', context)

@xframe_options_exempt
def serve_media(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path,'rb'))
    else:
        raise Http404("Media file not found.")
    

@login_required
def close_posting(request,job_id):
    job = get_object_or_404(Job, id = job_id)
    job.is_active = False
    job.save()
    messages.success(request, "Closing Sucessful!")

    return redirect('accounts:dashboard')


@login_required
def jobs_list(request):
    jobs = Job.objects.filter(created_by = request.user).order_by('-created_at')

    context = {
        'jobs' : jobs
    }

    return render(request, 'jobs/jobs_list.html', context)

@login_required
def screening_list(request):
    jobs = Job.objects.filter(created_by = request.user).order_by('-created_at')

    context = {
        'jobs' : jobs
    }

    return render(request, 'jobs/screening_jobs.html', context)

@login_required
def top_candidates_list(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    resumes = Resumes.objects.filter(job=job).order_by('-match_score')
    
    context = {
        'job': job,
        'resumes': resumes
    }
    return render(request, 'jobs/top_candidates_list.html', context)
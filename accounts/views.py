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

@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        user.profile_pictures = request.FILES.get('profile_picture')
        user.bio = request.POST.get('bio')
        user.save()

        messages.success(request,"Profile updated successfully!")
        return redirect("accounts:profile")

    return render(request,'accounts/profile.html', {'user': user}) 
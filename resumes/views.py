from django.shortcuts import render
from .models import Resumes
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def reseumes_list(request):
    resumes = Resumes.objects.filter(uploaded_by = request.user)

    context = {
        'resumes' : resumes
    }

    return render(request, 'resumes/resumes_list.html', context)
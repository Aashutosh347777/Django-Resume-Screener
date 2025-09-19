from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Resumes
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
import PyPDF2
from docx import Document
import re

# Create your views here.
def extract_text_from_file(file_obj):
    try:
        # check if the file is pdf
        if file_obj.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file_obj)
            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            return text
        
        # check if the file is a docx file
        elif file_obj.name.endswith('.docx'):
            doc = Document(file_obj)
            text = ""
            
            for para in doc.paragraphs:
                text += para.text + "\n"
            
            return text
        
        # handle the usupported file types 
        else:
            return "Unsupported file format!"

    except Exception as e:
        # log the error
        print(f"Error duing the file text extraction: {e}")
        return ""
    

def extract_resume_details(text):
    email = None
    phone = None
    name = "Unknown Candidate"

    # regex for email extraction
    emial_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if emial_match:
        email = emial_match.group(0)
    
    # regex for phone number extraction
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        phone = phone_match.group(0)

    name_match = re.search(r'^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+', text)
    if name_match:
        name = name_match.group(0)

    return {
        'name': name,
        'email': email,
        'phone': phone
    }


@login_required
def reseumes_list(request):
    resumes = Resumes.objects.filter(uploaded_by = request.user)

    context = {
        'resumes' : resumes
    }

    return render(request, 'resumes/resumes_list.html', context)


@login_required
def flagged_resumes(request):
        if request.user.role != 'recruiter':
            return HttpResponse("You are not authorized to view this page.", status=403)
        
        # filtering the resumes with match score 0 or None
        resumes = Resumes.objects.filter(Q(uploaded_by = request.user) & (Q(match_score =0.0) | Q(match_score__isnull = True )) )

        context = {
            'resumes' : resumes
        }

        return render(request, 'resumes/flagged_resumes.html', context)

@login_required
def rescreen_resume(request,resume_id):
    if request.user.role != 'recruiter':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('resumes:resumes_list')
    
    resume = get_object_or_404(Resumes, id = resume_id, uploaded_by = request.user)

    # hadling post request for rescreening
    if request.method == "POST":
        api_url = "http://127.0.0.1:8001/score"

        # getting job and resume information again
        job_text = f"{resume.job.title} {resume.job.description} {resume.job.requirements} {resume.job.location} {resume.job.employment_type}"
        resume_text = resume.parsed_text

        # posting in api
        try:
            payload = {
                "job_description_text" : job_text,
                "resume_text" : resume_text
            }
            response = requests.post(api_url, json = payload)
            response.raise_for_status() # raise for any exception
            match_score = response.json().get('score', 0.0) * 100

            # updating the new score
            resume.match_score = match_score
            resume.save()
            messages.success(request, f"Resume for {resume.candidate_name} re-screened successfully! New score: {match_score:.2f}%")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to FastAPI API: {e}")
            messages.error(request, f"Failed to get a new match score. Please check the API server.")

    return redirect('resumes:flagged_resumes')
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Resumes
from jobs.models import Job
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
        # log the error for debugging
        print(f"Error during file text extraction: {e}")
        return ""
    

def extract_resume_details(text):
    email = None
    phone = None
    name = "Unknown Candidate"
    skill = None
    work_experience = None
    education = None
    
    # Simple regex for email extraction
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        email = email_match.group(0)

    # Simple regex for phone number extraction (e.g., xxx-xxx-xxxx, (xxx) xxx-xxxx, xxxxxxxxxx)
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        phone = phone_match.group(0)

    # pattern looks for capitalized words at the start of the text
    name_match = re.search(r'^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+', text)
    if name_match:
        name = name_match.group(0)

    # pattern for skill
    skills_match = re.search(r'(?:skills?)(.*?)(?:work experience|education|projects|summary|\Z)', text, re.I | re.S)
    if skills_match:
        skill = skills_match.group(1).strip()
    
    # Work Experience section
    work_exp_match = re.search(r'(?:work\s*experience|professional\s*experience)(.*?)(?:education|skills|projects|summary|\Z)', text, re.I | re.S)
    if work_exp_match:
        work_experience = work_exp_match.group(1).strip()
    
    # Education section
    education_match = re.search(r'(?:education)(.*?)(?:work experience|skills|projects|summary|\Z)', text, re.I | re.S)
    if education_match:
        education = education_match.group(1).strip()

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'skill': skill,
        'work_experience': work_experience,
        'education' : education
    }


@login_required
def resume_detials(request, resume_id):
    # getting resume id 
    resume = get_object_or_404(Resumes, id = resume_id)

    context = {
        'resume' : resume
    }

    return render(request, 'resumes/resume_details.html', context)


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


@login_required
def upload_resume(request):
    if request.method == "POST":
        # form = ResumeUploadForm(request.POST, request.FILES)
        job_id = request.POST.get('job_id')
        resume_files = request.FILES.getlist('resume_files')

        if not job_id and resume_files:
            messages.error("Please make the entries!")
            return redirect('jobs:upload_resume')
        
        try:
            job = Job.objects.get(id = job_id)
            api_url = "http://127.0.0.1:8001/score"  # URL of your FastAPI server
            
            for resume_file in resume_files:
                # extract text from the resume
                parsed_text = extract_text_from_file(resume_file)   

                # resume information
                details = extract_resume_details(parsed_text)

                # Make a ppst request to the FastAPI API to get the match score
                payload = {
                    "job_description_text": f"{job.title} {job.description} {job.requirements} {job.location} {job.employment_type}",
                    "resume_text": parsed_text
                }
            
                match_score = 0.0
                try:
                    response = requests.post(api_url, json=payload)
                    response.raise_for_status() # Raise an exception for bad status codes
                    match_score = response.json().get('score', 0.0) * 100 # Convert to percentage
                except requests.exceptions.RequestException as e:
                    print(f"Error connecting to FastAPI API: {e}")
                    messages.error(request, "Failed to get a match score from the API. Please check the API server.")
                
                # resume object
                Resumes.objects.create(
                    uploaded_by=request.user,
                    job=job,
                    resume_files=resume_file,
                    parsed_text=parsed_text,
                    candidate_name=details['name'],
                    email=details['email'],
                    phone=details['phone'],
                    skill = details['skill'],
                    work_experience = details['work_experience'],
                    education = details['education'],

                    ats_score=0.0, # Placeholder for now, can be used for ATS score
                    match_score=match_score
                )
            messages.success(request, f"Resume uploaded and screened successfully! Match score: {match_score:.2f}%")
            return redirect('accounts:dashboard')

        except Job.DoesNotExist:
            messages.error(request, "Selected Job doesn't exist.")
            return redirect('jobs:upload_resume')
    # fetch all the jobs to display
    jobs = Job.objects.filter(is_active = True)
    context = {
        'jobs': jobs
    }
 
    return render(request, 'resumes/upload_resume.html', context)
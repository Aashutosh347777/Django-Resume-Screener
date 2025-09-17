from django.shortcuts import render, redirect
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
def upload_resume(request):
    if request.method == "POST":
        job_id = request.POST.get('job_id')
        resume_file = request.FILES.get('resume_file')

        if not job_id and resume:
            messages.error("Please make the entries!")
            return redirect('jobs:upload_resume')
        
        try:
            job = Job.objects.get(id = job_id)
            # extract text from the resume
            parsed_text = extract_text_from_file(resume_file)   

            # resume information
            details = extract_resume_details(parsed_text)

                        # Make a POST request to the FastAPI API to get the match score
            api_url = "http://127.0.0.1:8001/score"  # URL of your FastAPI server
            payload = {
                "job_description_text": f"{job.title} {job.description}",
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
            resume = Resumes.objects.create(
                uploaded_by=request.user,
                job=job,
                resume_files=resume_file,
                parsed_text=parsed_text,
                candidate_name=details['name'],
                email=details['email'],
                phone=details['phone'],
                ats_score=0.0, # Placeholder for now, can be used for ATS score
                match_score=match_score
            )
            messages.success(request, f"Resume uploaded and screened successfully! Match score: {match_score:.2f}%")
            return redirect('accounts:dashboard')

        except Job.DoesNotExist:
            messages.error(request, "Selected Job doesn't exist.")
            return redirect('jobs:upload_resume')
    # fetch all the jobs to display
    jobs = Job.objects.all()
    context = {
        'jobs': jobs
    }
 
    return render(request, 'jobs/upload_resume.html', context)

def extract_text_from_file(file_obj):
    """
    Extracts text from an uploaded file object.
    Supports PDF and DOCX formats.
    """
    try:
        # Check if the file is a PDF
        if file_obj.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file_obj)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        
        # Check if the file is a DOCX
        elif file_obj.name.endswith('.docx'):
            doc = Document(file_obj)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        
        # Handle unsupported file types gracefully
        else:
            return "Unsupported file format!"

    except Exception as e:
        # Log the error for debugging
        print(f"Error during file text extraction: {e}")
        return ""
    

def extract_resume_details(text):
    """
    Extracts candidate name, email, and phone number using regex patterns.
    """
    email = None
    phone = None
    name = "Unknown Candidate"
    
    # Simple regex for email extraction
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        email = email_match.group(0)

    # Simple regex for phone number extraction (e.g., xxx-xxx-xxxx, (xxx) xxx-xxxx, xxxxxxxxxx)
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        phone = phone_match.group(0)

    # Simple regex for name extraction (often at the beginning, may need refinement)
    # This pattern looks for capitalized words at the start of the text
    name_match = re.search(r'^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+', text)
    if name_match:
        name = name_match.group(0)

    return {
        'name': name,
        'email': email,
        'phone': phone
    }
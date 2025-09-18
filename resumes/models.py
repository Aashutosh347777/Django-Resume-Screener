from django.db import models
from django.conf import settings
from jobs.models import Job

# Create your models here.
class Resumes(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name= 'resumes')
    # linking resumes to the account who uploaded it

    resume_files = models.FileField(upload_to= "resume/")

    # link to jobs
    job = models.ForeignKey(Job, on_delete = models.SET_NULL,  null = True, blank = True, related_name='job_resumes')

    # add parsed_text field (extracting the plain text using ocr from resumes)
    parsed_text = models.TextField(blank = True, null = True)

    # details of the candidate field
    candidate_name = models.CharField(max_length= 50, blank=True, null= True)
    email = models.EmailField(blank=True, null = True)
    skill = models.TextField(blank= True, null= True )
    phone = models.CharField(max_length= 50, blank=True, null= True)

    # resume dates
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    # add scoring fields after ai assessment
    ats_score = models.FloatField(blank=True, null= True)
    match_score = models.FloatField(blank=True, null= True)
    
    def __str__(self):
        if self.candidate_name == None:
            return f"Resume of Unknown."
        else:
            return f"Resume of {self.candidate_name}."  

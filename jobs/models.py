from django.db import models
from django.conf import settings
# Create your models here.
class Job(models.Model):
    # linking job and hr
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE, related_name= 'jobs')

    # core information about the job
    title = models.CharField(max_length=100)
    description = models.TextField()  #not null in form and database
    requirements = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    choices_emp_type = [("FT",'Full-Time'),('PT','Part-Time'),('CT','Cotract')]
    employment_type = models.CharField(max_length= 50, choices= choices_emp_type, default="FT")

    # additional information
    salary_range = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # creation and updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        if self.location == None:
            return f"{self.title} 'Remote'"
        else:
            return f"{self.title} ({self.location})" 

    @property    
    def resumes_count(self):
        return self.job_resumes.count()
        # works since resume has a job foreign key

class Resume(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_resumes')
    full_name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume for {self.full_name} for {self.job.title}"

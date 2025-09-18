from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

role_choices = [('admin','Admin'),
                ('hr','HR'),
                ('recruiter','Recruiter')
]

# custom user model
class CustomUser(AbstractUser):
    role = models.CharField(max_length = 20, choices= role_choices, default = 'recruiter')
    profile_pictures = models.ImageField(upload_to = "profile_pics/", blank = True, null = True)
    bio = models.TextField(max_length = 200, blank = True)

    def __str__(self):
        return f"{self.username} ({self.role})"
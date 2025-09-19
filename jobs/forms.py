from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','description','requirements','location','employment_type','salary_range']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Senior Software Engineer'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Provide a detailed job description...'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List required skills and qualifications...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., San Francisco, CA or Remote'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., $100,000 - $120,000'}),
        }


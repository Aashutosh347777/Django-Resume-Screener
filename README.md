Resume Screener and Job Matching Platform
# Overview
The Resume Screener is a specialized web application built with Django that streamlines the hiring process by facilitating job management, resume uploads, and AI-powered candidate screening. It utilizes role-based access control (HR vs. Recruiter) and leverages external API services (like Gemini or OpenAI) to calculate a "match score" between job descriptions and uploaded resumes.

# Key Features
Role-Based Access
HR (Human Resources): Can post, view, and manage job listings.

Recruiter: Can upload resumes for specific job listings and view match scores only for the resumes they uploaded.

Job Management
Job Posting: Dedicated page for HRs to post new job openings with detailed descriptions, requirements, and salary information.

Job Dashboard: HRs get an overview of all jobs posted and the number of resumes applied to each.

AI-Powered Resume Screening
Resume Upload: Recruiters upload candidate resumes (PDF or DOCX).

Text Extraction: Resumes are automatically parsed to extract plain text content, candidate details (name, email, phone), skills, and work experience.

Smart Matching: The system calculates a Match Score using cosine similarity between the resume text and the target job description.

Rescreening: Recruiters can rescreen an existing resume against a different job they have posted.

User & Profile Management
Profile Editing: Users can update their bio and profile picture through a dedicated profile view.

Secure Media Serving: Custom view implemented to securely serve user-uploaded media (like resumes) during development and handle cross-origin framing for resume display (@xframe_options_exempt).

# Core Technologies
Backend Framework: Django (Python)

Database: Configured via Django settings (e.g., SQLite, PostgreSQL)

Frontend: HTML, Bootstrap (for styling and responsive design)

AI/NLP Services: External API calls (simulated via screening/services.py which interfaces with LLMs) for scoring.

File Parsing: Libraries for handling PDF and DOCX files.

Custom User Model: Uses a custom user model to implement roles (hr, recruiter).

# Setup and Installation
Follow these steps to set up the project environment and run the application locally.

1. Prerequisites
Python (3.8+)

pip (Python package installer)

2. Clone the Repository
git clone <Aashutosh347777/Django-Resume-Screener>
cd resume_screener

3. Virtual Environment
It is highly recommended to use a virtual environment:

python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows

4. Install Dependencies
Install all required Python packages:

pip install -r requirements.txt

(Note: A requirements.txt file is assumed to exist with Django, Pillow, python-docx, and other necessary packages).

5. Database Setup
Apply the database migrations:

python manage.py makemigrations
python manage.py migrate

6. Create Superuser (Admin Access)
python manage.py createsuperuser

7. Run the Server
Start the development server:

python manage.py runserver

The application will be available at http://localhost:8000/.

# Usage
Logging In
Access the login page at http://localhost:8000/

Role, Permissions & Dashboard

HR

Can post new jobs, see a list of all jobs, and view all system activity.

Recruiter

Can upload resumes, view only the resumes they uploaded, and rescreen candidates against different jobs.

Testing Different User Roles Simultaneously
To avoid session conflicts when testing both HR and Recruiter accounts at the same time, always use an Incognito/Private browser window for the second account.

Debugging Notes
If you encounter AttributeError: 'NoneType' object has no attribute 'strip' during resume upload, it indicates that the custom regex patterns in resumes/views.py failed to find a content section (Skills, Work Experience, or Education). This is typically due to unusual resume formatting.
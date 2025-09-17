import pickle
import ast
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
from io import StringIO
import pandas as pd
import os
import re

# fast api instance
app = FastAPI(title = "Resume Screener model API")

# model path
MODEL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'screener.pkl')

# try catch for loading the model
tfidf_vectorizer = None
try:
    with open(MODEL_FILE_PATH, 'rb') as file:
        tfidf_vectorizer = pickle.load(file)
except FileNotFoundError:
    raise RuntimeError(f"Vectorizer model not found at {MODEL_FILE_PATH}. Please train and save it first.")
except Exception as e:
    raise RuntimeError(f"Failed to load the model using pickle: {e}")

# verifying the correct format of incomming data
class ScoreRequest(BaseModel):
    job_description_text: str
    resume_text: str

def clean_and_preprocess(text):
    """
    Cleans a string by removing newlines, extra spaces, and special characters.
    This function is now a unified method to ensure consistency between
    job description and resume text preprocessing.
    """
    text = str(text).lower()
    text = text.replace("\n", " ")  # Replace newlines with spaces
    text = re.sub(r'[^a-z0-9\s]', '', text) # Remove special characters
    words = text.split()  # Splits the string by any whitespace and removes empty strings
    cleaned_text = " ".join(words)  # Joins the words with a single space
    return cleaned_text


@app.post("/score")
def score_texts(request: ScoreRequest):
    """
    Calculates the cosine similarity score between a job description and a resume.
    """
    if tfidf_vectorizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Server is not ready.")

    try:
        # Preprocess the input texts using the unified function
        clean_job_text = clean_and_preprocess(request.job_description_text)
        clean_resume_text = clean_and_preprocess(request.resume_text)

        # Transform the cleaned texts into vectors using the loaded vectorizer
        job_vector = tfidf_vectorizer.transform([clean_job_text])
        resume_vector = tfidf_vectorizer.transform([clean_resume_text])
        
        # Calculate the cosine similarity score
        score = cosine_similarity(job_vector, resume_vector)[0][0]
        
        # Return the score as a JSON response
        return {"score": score}

    except Exception as e:
        # Handle any unexpected errors and return a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
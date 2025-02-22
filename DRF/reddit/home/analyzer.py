import pdfplumber
import spacy
import base64
import uuid
from groq import Groq
import os, sys
import json


nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def analyze_resume(text):
    doc = nlp(text)
    skills = [token.text for token in doc.ents if token.label_ == "SKILL"]
    experience = [sent.text for sent in doc.sents if "years" in sent.text.lower()]
    education = [sent.text for sent in doc.sents if "university" in sent.text.lower()]
    return {
        "skills": ", ".join(skills),
        "experience": "\n".join(experience),
        "education": "\n".join(education),
    }




def analyze_resume_with_llm(resume_text: str, job_description: str) -> dict:
    """
    Analyzes a resume using an LLM based on the given job description.
    
    Args:
        resume_text (str): Extracted text from a resume.
        job_description (str): Job description text.
    
    Returns:
        dict: JSON response with skills, experience, project domains, and ranking.
    """
    prompt = f"""
    You are an AI assistant that analyzes resumes for software engineering job applications. 
    Given a resume and a job description, extract the following details:
    
    1. Identify all skills mentioned in the resume.
    2. Calculate the total years of experience.
    3. Categorize the projects based on domain (e.g., AI, Web Development, Cloud, etc.).
    4. Rank the resume's relevance to the job description on a scale of 0 to 100%.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}

    Provide the output in valid JSON format with this structure:
    {{
        "rank": "<percentage>",
        "skills": ["skill1", "skill2", ...],
        "total_experience": "<number of years>",
        "project_category": ["category1", "category2", ...]
    }}
    """

    try:
        client = Groq(api_key="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")
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        result = response.choices[0].message.content
        return json.loads(result)  # Convert string response to dictionary

    except Exception as e:
        print(f"Error processing resume: {e}")
        return {"error": "Failed to analyze resume"}

import os , sys

def process_resume(pdf_path, job_description):
    try:
        text = extract_text_from_pdf(pdf_path)
        analysis = analyze_resume(text)
        data = analyze_resume_with_llm(text , job_description)
        return data
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
        return None

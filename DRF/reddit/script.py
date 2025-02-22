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


def process_resume():
    pdf_path = 'abhijeet_gupta_resume.pdf'
    text = extract_text_from_pdf(pdf_path)
    analysis = analyze_resume(text)
    job_description = """
        Job Description: Lead Frontend Developer (10+ Years of Experience)
Location: [Specify Location or Remote]
Employment Type: Full-time
Experience Required: 10+ Years
Salary: [Specify Salary Range]
About the Role
We are looking for an experienced Lead Frontend Developer with 10+ years of expertise in building modern, scalable, and high-performance web applications. You will lead the frontend development team, drive architectural decisions, mentor junior developers, and collaborate closely with backend engineers, designers, and product managers to create seamless user experiences.

Key Responsibilities
Architect and develop highly responsive, user-friendly web applications using modern frontend technologies.
Lead and mentor a team of frontend developers, conducting code reviews and enforcing best practices.
Optimize performance of web applications for maximum speed and scalability.
Collaborate with UI/UX designers and backend engineers to ensure smooth integration of APIs and user interfaces.
Stay up-to-date with the latest frontend technologies, frameworks, and industry trends.
Ensure cross-browser compatibility and responsiveness of applications.
Write clean, maintainable, and well-documented code following best coding practices.
Drive innovation by suggesting and implementing new tools, frameworks, and methodologies.
Required Skills & Experience
10+ years of experience in frontend development.
Expertise in JavaScript, TypeScript, HTML5, and CSS3.
Strong experience with modern frontend frameworks: React.js, Vue.js, or Angular.
Deep understanding of state management libraries like Redux, Vuex, or Zustand.
Proficiency in building reusable UI components and scalable frontend architectures.
Experience with performance optimization techniques, lazy loading, code splitting, etc.
Knowledge of frontend build tools like Webpack, Vite, Babel, and Parcel.
Familiarity with CI/CD pipelines and DevOps practices for frontend deployment.
Experience with testing frameworks (Jest, Cypress, React Testing Library, etc.).
Good understanding of RESTful APIs & GraphQL.
Experience with micro-frontends and modular frontend architectures is a plus.
Familiarity with accessibility (WCAG) and internationalization (i18n).
Excellent problem-solving skills, leadership, and ability to work in an agile environment.
Preferred Qualifications
Experience with WebAssembly (WASM) and WebSockets.
Knowledge of server-side rendering (SSR) using Next.js or Nuxt.js.
Familiarity with cloud platforms (AWS, GCP, Azure).
Experience in headless CMS and JAMstack architecture.
Why Join Us?
Opportunity to lead a cutting-edge frontend team.
Work on high-impact, large-scale projects.
Collaborative and innovative work environment.
Competitive salary, benefits, and learning opportunities.
If you are passionate about building world-class web applications and leading a team of talented developers, we'd love to hear from you! 🚀
    """
    data = analyze_resume_with_llm(text , job_description)
    print(data)

process_resume()
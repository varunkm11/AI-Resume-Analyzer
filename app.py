from flask import Flask, request, render_template, jsonify
import os
import PyPDF2
import re
import json
from werkzeug.utils import secure_filename
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Job role keywords and requirements
JOB_ROLES = {
    "Software Engineer": {
        "technical_skills": ["python", "java", "javascript", "react", "node.js", "sql", "git", "api", "database", "algorithm", "data structure", "object-oriented", "agile", "scrum", "testing", "debugging", "cloud", "aws", "docker", "kubernetes"],
        "soft_skills": ["problem solving", "teamwork", "communication", "leadership", "analytical", "creative", "adaptable"],
        "experience_keywords": ["developed", "implemented", "designed", "created", "built", "optimized", "maintained", "collaborated", "led", "managed"],
        "education_keywords": ["computer science", "software engineering", "information technology", "computer engineering", "bachelor", "master", "degree"]
    },
    "Data Scientist": {
        "technical_skills": ["python", "r", "sql", "machine learning", "deep learning", "tensorflow", "pytorch", "pandas", "numpy", "matplotlib", "seaborn", "jupyter", "statistics", "data analysis", "data visualization", "big data", "hadoop", "spark", "tableau", "power bi"],
        "soft_skills": ["analytical", "problem solving", "communication", "critical thinking", "attention to detail", "creativity"],
        "experience_keywords": ["analyzed", "modeled", "predicted", "visualized", "interpreted", "extracted", "cleaned", "processed", "researched", "experimented"],
        "education_keywords": ["data science", "statistics", "mathematics", "computer science", "physics", "engineering", "bachelor", "master", "phd", "degree"]
    },
    "Digital Marketing": {
        "technical_skills": ["google analytics", "seo", "sem", "social media", "facebook ads", "google ads", "email marketing", "content marketing", "wordpress", "html", "css", "photoshop", "canva", "hootsuite", "mailchimp"],
        "soft_skills": ["creativity", "communication", "analytical", "strategic thinking", "adaptability", "attention to detail"],
        "experience_keywords": ["managed", "created", "optimized", "increased", "generated", "developed", "executed", "analyzed", "coordinated", "launched"],
        "education_keywords": ["marketing", "business", "communications", "advertising", "media", "bachelor", "master", "degree", "certification"]
    },
    "Project Manager": {
        "technical_skills": ["project management", "agile", "scrum", "kanban", "jira", "trello", "microsoft project", "gantt charts", "risk management", "budget management", "stakeholder management", "pmp", "prince2"],
        "soft_skills": ["leadership", "communication", "organization", "problem solving", "negotiation", "time management", "teamwork"],
        "experience_keywords": ["managed", "led", "coordinated", "planned", "executed", "delivered", "organized", "facilitated", "monitored", "controlled"],
        "education_keywords": ["project management", "business administration", "engineering", "management", "bachelor", "master", "degree", "certification", "pmp"]
    },
    "UX/UI Designer": {
        "technical_skills": ["figma", "sketch", "adobe xd", "photoshop", "illustrator", "prototyping", "wireframing", "user research", "usability testing", "html", "css", "javascript", "responsive design", "mobile design"],
        "soft_skills": ["creativity", "empathy", "communication", "problem solving", "attention to detail", "collaboration"],
        "experience_keywords": ["designed", "created", "developed", "researched", "tested", "collaborated", "improved", "optimized", "conceptualized", "implemented"],
        "education_keywords": ["design", "user experience", "human-computer interaction", "graphic design", "visual arts", "psychology", "bachelor", "master", "degree"]
    }
}

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ""

def preprocess_text(text):
    """Clean and preprocess text"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    return tokens

def calculate_ats_score(resume_text, job_role):
    """Calculate ATS score based on job role requirements"""
    if job_role not in JOB_ROLES:
        return {"error": "Invalid job role"}
    
    role_requirements = JOB_ROLES[job_role]
    resume_tokens = preprocess_text(resume_text)
    resume_text_lower = resume_text.lower()
    
    scores = {}
    total_score = 0
    max_possible_score = 0
    
    # Technical Skills (40% weight)
    technical_matches = 0
    for skill in role_requirements["technical_skills"]:
        if skill.lower() in resume_text_lower:
            technical_matches += 1
    
    technical_score = (technical_matches / len(role_requirements["technical_skills"])) * 40
    scores["technical_skills"] = {
        "score": round(technical_score, 1),
        "matches": technical_matches,
        "total": len(role_requirements["technical_skills"])
    }
    total_score += technical_score
    max_possible_score += 40
    
    # Soft Skills (20% weight)
    soft_matches = 0
    for skill in role_requirements["soft_skills"]:
        if skill.lower() in resume_text_lower:
            soft_matches += 1
    
    soft_score = (soft_matches / len(role_requirements["soft_skills"])) * 20
    scores["soft_skills"] = {
        "score": round(soft_score, 1),
        "matches": soft_matches,
        "total": len(role_requirements["soft_skills"])
    }
    total_score += soft_score
    max_possible_score += 20
    
    # Experience Keywords (25% weight)
    experience_matches = 0
    for keyword in role_requirements["experience_keywords"]:
        if keyword.lower() in resume_text_lower:
            experience_matches += 1
    
    experience_score = (experience_matches / len(role_requirements["experience_keywords"])) * 25
    scores["experience"] = {
        "score": round(experience_score, 1),
        "matches": experience_matches,
        "total": len(role_requirements["experience_keywords"])
    }
    total_score += experience_score
    max_possible_score += 25
    
    # Education (15% weight)
    education_matches = 0
    for keyword in role_requirements["education_keywords"]:
        if keyword.lower() in resume_text_lower:
            education_matches += 1
    
    education_score = (education_matches / len(role_requirements["education_keywords"])) * 15
    scores["education"] = {
        "score": round(education_score, 1),
        "matches": education_matches,
        "total": len(role_requirements["education_keywords"])
    }
    total_score += education_score
    max_possible_score += 15
    
    # Calculate overall ATS score
    ats_score = round(total_score, 1)
    
    # Generate recommendations
    recommendations = generate_recommendations(scores, role_requirements)
    
    return {
        "ats_score": ats_score,
        "breakdown": scores,
        "recommendations": recommendations,
        "job_role": job_role
    }

def generate_recommendations(scores, role_requirements):
    """Generate improvement recommendations based on scores"""
    recommendations = []
    
    if scores["technical_skills"]["score"] < 20:
        recommendations.append("Add more relevant technical skills to your resume")
    
    if scores["soft_skills"]["score"] < 10:
        recommendations.append("Include more soft skills and interpersonal abilities")
    
    if scores["experience"]["score"] < 15:
        recommendations.append("Use more action verbs to describe your experience")
    
    if scores["education"]["score"] < 8:
        recommendations.append("Highlight your educational background more prominently")
    
    if not recommendations:
        recommendations.append("Great job! Your resume is well-optimized for this role.")
    
    return recommendations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['resume']
        job_role = request.form.get('job_role')
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if job_role not in JOB_ROLES:
            return jsonify({"error": "Invalid job role selected"}), 400
        
        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract text from PDF
            resume_text = extract_text_from_pdf(file_path)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            if not resume_text.strip():
                return jsonify({"error": "Could not extract text from PDF"}), 400
            
            # Calculate ATS score
            result = calculate_ats_score(resume_text, job_role)
            
            return jsonify(result)
        
        else:
            return jsonify({"error": "Please upload a PDF file"}), 400
    
    except Exception as e:
        logging.error(f"Error analyzing resume: {e}")
        return jsonify({"error": "An error occurred while analyzing the resume"}), 500

@app.route('/job-roles')
def get_job_roles():
    return jsonify(list(JOB_ROLES.keys()))

if __name__ == '__main__':
    app.run(debug=True)

# AI Resume Analyzer

A minimalist web application that analyzes resumes and provides ATS (Applicant Tracking System) scores based on job roles. Upload your PDF resume, select a target job role, and get detailed feedback on how to improve your resume for better ATS compatibility.

## 🚀 Live Demo

**Try it now:** [https://ai-resume-analyzer-coj73erz4.vercel.app](https://ai-resume-analyzer-coj73erz4.vercel.app)

## Features

- **ATS Score Calculation**: Get a comprehensive score based on technical skills, soft skills, experience, and education
- **Job Role Specific Analysis**: Analyze your resume against specific job roles:
  - Software Engineer
  - Data Scientist
  - Digital Marketing
  - Project Manager
  - UX/UI Designer
- **Detailed Breakdown**: See exactly where your resume scores well and where it needs improvement
- **Actionable Recommendations**: Get specific suggestions to improve your ATS score
- **Minimalist Design**: Clean, modern interface that's easy to use
- **PDF Support**: Upload PDF resumes for analysis

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Resume-Analyzer
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## How It Works

### ATS Scoring Algorithm

The application analyzes your resume using a weighted scoring system:

- **Technical Skills (40%)**: Matches job-specific technical skills and tools
- **Soft Skills (20%)**: Identifies important interpersonal and professional skills
- **Experience Keywords (25%)**: Looks for action verbs and experience-related terms
- **Education (15%)**: Checks for relevant educational background and qualifications

### Job Roles Supported

1. **Software Engineer**: Python, Java, JavaScript, React, APIs, databases, cloud technologies
2. **Data Scientist**: Python, R, machine learning, statistics, data visualization, big data tools
3. **Digital Marketing**: SEO, SEM, social media, analytics, content marketing, advertising platforms
4. **Project Manager**: Project management methodologies, tools, leadership, stakeholder management
5. **UX/UI Designer**: Design tools, user research, prototyping, usability testing, design thinking

## Usage

1. **Select Job Role**: Choose the target job role you want to analyze against
2. **Upload Resume**: Upload your resume in PDF format (max 16MB)
3. **Get Analysis**: Click "Analyze Resume" to get your ATS score
4. **Review Results**: See your overall score, detailed breakdown, and recommendations
5. **Improve**: Use the recommendations to enhance your resume

## Technical Details

### Backend
- **Flask**: Web framework for the backend API
- **PyPDF2**: PDF text extraction
- **NLTK**: Natural language processing for text analysis
- **Python**: Core language for analysis algorithms

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript**: Interactive functionality and API communication
- **Font Awesome**: Icons for better visual appeal

### File Structure
```
AI-Resume-Analyzer/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── script.js     # Frontend JavaScript
└── uploads/              # Temporary file storage (auto-created)
```

## Customization

### Adding New Job Roles

To add a new job role, modify the `JOB_ROLES` dictionary in `app.py`:

```python
JOB_ROLES["New Role"] = {
    "technical_skills": ["skill1", "skill2", ...],
    "soft_skills": ["skill1", "skill2", ...],
    "experience_keywords": ["keyword1", "keyword2", ...],
    "education_keywords": ["keyword1", "keyword2", ...]
}
```

### Adjusting Score Weights

Modify the scoring weights in the `calculate_ats_score` function:

```python
technical_score = (technical_matches / len(role_requirements["technical_skills"])) * 40  # 40% weight
soft_score = (soft_matches / len(role_requirements["soft_skills"])) * 20              # 20% weight
experience_score = (experience_matches / len(role_requirements["experience_keywords"])) * 25  # 25% weight
education_score = (education_matches / len(role_requirements["education_keywords"])) * 15     # 15% weight
```

## Security Considerations

- Files are temporarily stored and immediately deleted after processing
- File size is limited to 16MB
- Only PDF files are accepted
- Input validation and sanitization is implemented

## Future Enhancements

- Support for more file formats (DOCX, TXT)
- Integration with AI models for more sophisticated analysis
- Resume optimization suggestions
- Comparison with industry benchmarks
- Export analysis reports
- User accounts and resume history

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or issues, please open an issue on the GitHub repository or contact the development team.

---

## 👨‍💻 Developer

**Developed by:** Varun Kumar Singh  
**Email:** varunkumarsingh818@gmail.com  
**GitHub:** [@varunkumarsingh](https://github.com/varunkumarsingh)  
**LinkedIn:** [Varun Kumar Singh](https://linkedin.com/in/varunkumarsingh)

---

**Note**: This tool provides general guidance for resume optimization. Results may vary depending on specific company requirements and ATS systems.

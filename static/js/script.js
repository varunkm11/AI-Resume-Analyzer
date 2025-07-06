// DOM Elements
const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const resumeForm = document.getElementById('resumeForm');
const resumeFile = document.getElementById('resumeFile');
const fileName = document.getElementById('fileName');
const jobRoleSelect = document.getElementById('jobRole');
const analyzeBtn = document.getElementById('analyzeBtn');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadJobRoles();
    setupFileUpload();
    setupFormSubmission();
});

// Load job roles from the backend
async function loadJobRoles() {
    try {
        const response = await fetch('/job-roles');
        const jobRoles = await response.json();
        
        jobRoles.forEach(role => {
            const option = document.createElement('option');
            option.value = role;
            option.textContent = role;
            jobRoleSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading job roles:', error);
        showError('Failed to load job roles');
    }
}

// Setup file upload functionality
function setupFileUpload() {
    resumeFile.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            if (file.type === 'application/pdf') {
                fileName.textContent = file.name;
                fileName.style.color = '#667eea';
            } else {
                fileName.textContent = 'Please select a PDF file';
                fileName.style.color = '#e53e3e';
                this.value = '';
            }
        } else {
            fileName.textContent = 'Choose PDF file';
            fileName.style.color = '#4a5568';
        }
    });
}

// Setup form submission
function setupFormSubmission() {
    resumeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        const formData = new FormData(this);
        
        // Show loading state
        showLoading();
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showResults(result);
            } else {
                showError(result.error || 'An error occurred while analyzing the resume');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please try again.');
        }
    });
}

// Validate form inputs
function validateForm() {
    const jobRole = jobRoleSelect.value;
    const file = resumeFile.files[0];
    
    if (!jobRole) {
        showError('Please select a job role');
        return false;
    }
    
    if (!file) {
        showError('Please upload a resume file');
        return false;
    }
    
    if (file.type !== 'application/pdf') {
        showError('Please upload a PDF file');
        return false;
    }
    
    // Check file size (16MB limit)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size must be less than 16MB');
        return false;
    }
    
    return true;
}

// Show loading state
function showLoading() {
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
    
    // Disable form submission
    analyzeBtn.disabled = true;
}

// Show results
function showResults(data) {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Update ATS score
    document.getElementById('atsScore').textContent = data.ats_score;
    document.getElementById('analyzedRole').textContent = data.job_role;
    
    // Update score circle color based on score
    const scoreCircle = document.querySelector('.score-circle');
    if (data.ats_score >= 70) {
        scoreCircle.style.background = 'linear-gradient(135deg, #4caf50 0%, #388e3c 100%)';
    } else if (data.ats_score >= 50) {
        scoreCircle.style.background = 'linear-gradient(135deg, #ff9800 0%, #f57c00 100%)';
    } else {
        scoreCircle.style.background = 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)';
    }
    
    // Update breakdown scores
    updateBreakdownItem('technical', data.breakdown.technical_skills);
    updateBreakdownItem('soft', data.breakdown.soft_skills);
    updateBreakdownItem('experience', data.breakdown.experience);
    updateBreakdownItem('education', data.breakdown.education);
    
    // Update recommendations
    updateRecommendations(data.recommendations);
    
    // Re-enable form submission
    analyzeBtn.disabled = false;
}

// Update breakdown item
function updateBreakdownItem(type, data) {
    const scoreElement = document.getElementById(`${type}Score`);
    const progressElement = document.getElementById(`${type}Progress`);
    const detailElement = document.getElementById(`${type}Detail`);
    
    scoreElement.textContent = `${data.score}/${getMaxScore(type)}`;
    progressElement.style.width = `${(data.score / getMaxScore(type)) * 100}%`;
    
    let itemType;
    switch(type) {
        case 'technical':
        case 'soft':
            itemType = 'skills';
            break;
        case 'experience':
            itemType = 'keywords';
            break;
        case 'education':
            itemType = 'keywords';
            break;
    }
    
    detailElement.textContent = `${data.matches} out of ${data.total} ${itemType} found`;
}

// Get maximum score for each category
function getMaxScore(type) {
    const maxScores = {
        'technical': 40,
        'soft': 20,
        'experience': 25,
        'education': 15
    };
    return maxScores[type];
}

// Update recommendations
function updateRecommendations(recommendations) {
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';
    
    recommendations.forEach(recommendation => {
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        item.innerHTML = `
            <i class="fas fa-lightbulb"></i>
            <p>${recommendation}</p>
        `;
        recommendationsList.appendChild(item);
    });
}

// Show error message
function showError(message) {
    // Create error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.innerHTML = `
        <div class="error-content">
            <i class="fas fa-exclamation-triangle"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Add error styles
    errorDiv.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        z-index: 1000;
        background: #fed7d7;
        color: #c53030;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #feb2b2;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    
    const errorContent = errorDiv.querySelector('.error-content');
    errorContent.style.cssText = `
        display: flex;
        align-items: center;
        gap: 0.75rem;
    `;
    
    const closeButton = errorContent.querySelector('button');
    closeButton.style.cssText = `
        background: none;
        border: none;
        color: #c53030;
        cursor: pointer;
        padding: 0.25rem;
        margin-left: auto;
    `;
    
    document.body.appendChild(errorDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 5000);
    
    // Reset loading state
    loadingSection.style.display = 'none';
    uploadSection.style.display = 'block';
    analyzeBtn.disabled = false;
}

// Analyze another resume
function analyzeAnother() {
    // Reset form
    resumeForm.reset();
    fileName.textContent = 'Choose PDF file';
    fileName.style.color = '#4a5568';
    
    // Show upload section
    resultsSection.style.display = 'none';
    uploadSection.style.display = 'block';
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .error-notification {
        animation: slideIn 0.3s ease;
    }
`;
document.head.appendChild(style);

# 🚀 Deploy AI Resume Analyzer to Vercel

This guide will help you deploy your AI Resume Analyzer to Vercel for free.

## Prerequisites

1. **GitHub Account**: You'll need a GitHub account to connect with Vercel
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com) (free)
3. **Git**: Make sure Git is installed on your computer

## Step 1: Push to GitHub

1. **Initialize Git Repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI Resume Analyzer"
   ```

2. **Create a new repository on GitHub**:
   - Go to [GitHub](https://github.com)
   - Click "New repository"
   - Name it "ai-resume-analyzer"
   - Don't initialize with README (we already have files)
   - Click "Create repository"

3. **Connect and push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy to Vercel

### Option A: Using Vercel CLI (Recommended)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from your project directory**:
   ```bash
   vercel
   ```
   
4. **Follow the prompts**:
   - Link to existing project? **N**
   - What's your project's name? **ai-resume-analyzer**
   - In which directory is your code located? **./**
   - Want to override the settings? **N**

### Option B: Using Vercel Dashboard

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**

2. **Click "New Project"**

3. **Import from GitHub**:
   - Connect your GitHub account if not already connected
   - Select your "ai-resume-analyzer" repository
   - Click "Import"

4. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: **./**
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`

5. **Click "Deploy"**

## Step 3: Environment Variables (Optional)

If you want to add environment variables:

1. Go to your project in Vercel Dashboard
2. Click on "Settings" tab
3. Click on "Environment Variables"
4. Add any variables you need:
   - `SECRET_KEY`: A secure random string

## Important Notes

### File Structure for Vercel
Your project should have this structure:
```
ai-resume-analyzer/
├── app.py              # Main Flask app
├── index.py            # WSGI entry point
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── README.md
```

### Vercel Configuration
The `vercel.json` file is configured to:
- Use Python runtime
- Route all requests to `app.py`
- Handle serverless deployment

### Performance Considerations
- First load might be slower (cold start)
- NLTK downloads happen on first request
- Files are processed in temporary storage
- Suitable for moderate traffic

### Limitations on Vercel
- **Function timeout**: 10 seconds on Hobby plan
- **File size**: 50MB limit per function
- **Memory**: 1024MB on Hobby plan
- **Bandwidth**: 100GB/month on free plan

## Step 4: Testing Your Deployment

1. **Wait for deployment to complete** (usually 1-2 minutes)

2. **Visit your app**:
   - Vercel will provide a URL like: `https://ai-resume-analyzer-xyz.vercel.app`

3. **Test the functionality**:
   - Upload a sample PDF resume
   - Select a job role
   - Check if analysis works correctly

## Troubleshooting

### Common Issues:

1. **NLTK Download Errors**:
   - The app includes fallback logic for NLTK failures
   - Basic text processing will still work

2. **PDF Processing Fails**:
   - Ensure PDF is not password-protected
   - Check file size (max 16MB)

3. **Deployment Fails**:
   - Check `requirements.txt` has all dependencies
   - Ensure `vercel.json` is in root directory

4. **Function Timeout**:
   - Large PDFs might timeout on processing
   - Consider optimizing PDF text extraction

### Updating Your App:

1. **Make changes locally**
2. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
3. **Vercel auto-deploys** from GitHub

## Custom Domain (Optional)

1. Go to your project in Vercel Dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Monitoring

- **Vercel Analytics**: Available in dashboard
- **Function Logs**: Check runtime logs for debugging
- **Performance**: Monitor response times and errors

Your AI Resume Analyzer is now live and accessible worldwide! 🎉

## Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Issues**: Check GitHub repository issues
- **Community**: Vercel Discord/GitHub Discussions

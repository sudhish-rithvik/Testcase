# TestCaseAI - Healthcare Test Case Generator

## 🏥 Overview
TestCaseAI is an AI-powered healthcare test case generation system that analyzes PDF documents and creates comprehensive, HIPAA-compliant test cases using Gemini 2.5 Flash.

## ✨ Features
- 📄 **PDF Upload** - Drag-and-drop PDF upload
- 🤖 **AI Generation** - Gemini 2.5 Flash generates comprehensive test cases
- ☁️ **AWS Storage** - S3 for files, DynamoDB for metadata
- 🏥 **Healthcare Focus** - HIPAA compliance, medication safety, security
- 📊 **Dashboard** - Statistics and recent activity
- 📜 **History** - View and download past test cases

## 🚀 Quick Start

### 1. Start Backend
```bash
cd backend
uvicorn app.main:app --reload --env-file .env
```

### 2. Open Frontend
```bash
cd frontend
# Open index.html in your browser
# Or use Live Server in VS Code
```

## 📁 Project Structure
```
 Testcase/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI app
│   ├── .env                 # Environment variables
│   └── requirements.txt
└── frontend/
    ├── index.html           # Dashboard
    ├── upload.html          # Upload page
    ├── testcases.html       # Test case viewer
    ├── history.html         # History page
    ├── css/
    │   └── styles.css
    └── js/
        ├── dashboard.js
        ├── upload.js
        ├── testcases.js
        └── history.js
```

## 🔧 Configuration
Edit `backend/.env`:
```env
GEMINI_API_KEY=your_key_here
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=eu-north-1
AWS_S3_BUCKET_NAME=testcaseai-pdf-storage
```

## 📖 Usage

1. **Upload** - Go to Upload page, drag-drop PDF
2. **Process** - AI extracts text and generates test cases
3. **View** - Test cases displayed in organized boxes
4. **Download** - Get JSON or Markdown format
5. **History** - Access past uploads anytime

## 🎨 UI Pages

- **Dashboard** - Statistics, quick actions, recent activity
- **Upload** - Drag-drop interface with progress tracking
- **Test Cases** - Organized boxes with clear formatting
- **History** - Search, filter, and download past files

## 🛠️ Tech Stack

**Backend:**
- FastAPI
- Python 3.x
- AWS S3 & DynamoDB
- Gemini 2.5 Flash AI

**Frontend:**
- Vanilla HTML/CSS/JavaScript
- Modern responsive design
- Healthcare-themed UI

## 📊 API Endpoints

- `POST /upload-pdf` - Upload and process PDF
- `GET /history` - Get upload history
- `GET /file/{file_id}` - Get file metadata
- `GET /download/testcases/{file_id}` - Download JSON
- `GET /download/markdown/{file_id}` - Download Markdown
- `GET /download/pdf/{file_id}` - Download original PDF

## 🎯 Healthcare Test Case Categories

1. ✅ Positive Test Cases
2. ❌ Negative Test Cases
3. 🔒 Security Test Cases
4. ⚡ Edge Cases & Boundaries
5. 🏥 Healthcare-Specific Scenarios
6. 🔄 Integration Tests
7. 💊 Medication Safety
8. 📊 Data Validation
9. 🎯 Implementation Notes
10. 🚨 Critical Issues

## 📝 License
MIT

## 👤 Author
Created with ❤️ for healthcare software testing

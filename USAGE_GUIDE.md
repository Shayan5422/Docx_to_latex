# 🚀 DOCX to LaTeX Web Application Usage Guide

## 📋 Table of Contents

1. [Running Backend and Frontend Separately](#separate-execution)
2. [Complete ZIP Package Downloads](#zip-download)
3. [Troubleshooting](#troubleshooting)

---

## 🔧 Running Backend and Frontend Separately {#separate-execution}

### 1️⃣ Starting the Backend

```bash
# Navigate to the project directory
cd /Users/shayanhashemi/Downloads/Docx_to_latex/Docx_to_latex

# Start the backend
python start_backend.py
```

**Successful output:**
```
🚀 DOCX to LaTeX - Backend API Server
============================================================
✅ Project root: /path/to/project
🔧 Starting backend server...
- API Server: http://localhost:5000
```

### 2️⃣ Starting the Frontend

**In a separate terminal:**
```bash
# In second terminal
cd /Users/shayanhashemi/Downloads/Docx_to_latex/Docx_to_latex

# Start the frontend
python start_frontend.py
```

**Successful output:**
```
🎨 DOCX to LaTeX - Frontend Web Interface
============================================================
✅ Node.js installed: v18.x.x
✅ Frontend directory: /path/to/frontend
🔧 Starting frontend server...
- Web Interface: http://localhost:3000
```

---

## 📦 Complete ZIP Package Downloads {#zip-download}

### New Feature: Complete Package

After successful conversion, you have two download options:

#### 🔹 LaTeX File Only
- Pure `.tex` file
- For advanced LaTeX users

#### 🔹 Complete Package (ZIP) ⭐ **Recommended**
Includes:
- 📄 Main LaTeX file
- 🖼️ All images in `media/` folder
- 📋 `README.txt` file with complete instructions
- ✅ Ready for Overleaf upload

### ZIP File Contents:

```
my-document_complete.zip
├── my-document.tex          # Main LaTeX file
├── media/                   # Images folder
│   ├── image1.png
│   ├── image2.jpg
│   └── ...
└── README.txt              # Usage instructions
```

### Using with Overleaf:

1. Extract the ZIP file
2. Upload all files to a new Overleaf project
3. Set main file: `your-document.tex`
4. Compile!

---

## 🔍 Troubleshooting {#troubleshooting}

### Common Issues

#### ❌ Backend won't start
```bash
# Check packages
pip install -r requirements_web.txt

# Check Pandoc
pandoc --version
```

#### ❌ Frontend won't start
```bash
# Check Node.js
node --version

# Reinstall dependencies
cd docx_to_latex
rm -rf node_modules
npm install
```

#### ❌ Port is occupied
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

#### ❌ "Failed to fetch" in browser
- Make sure backend is running on port 5000
- API address in frontend: `http://localhost:5000`

### API Health Check:

```bash
# Test API
curl http://localhost:5000/api/health
```

**Successful response:**
```json
{"status": "healthy", "message": "DOCX to LaTeX API is running"}
```

---

## 🎯 Usage Steps

### 1. Setup
```bash
# Terminal 1 - Backend
python start_backend.py

# Terminal 2 - Frontend  
python start_frontend.py
```

### 2. Using the Web Application
1. 🌐 Go to: `http://localhost:3000`
2. 📁 Drag & drop your DOCX file
3. ⚙️ Check settings (default: all enabled)
4. 🚀 Click "Convert to LaTeX"
5. 📦 Download "Complete Package (ZIP)"

### 3. Using Generated Files
- Extract ZIP
- Upload to Overleaf or compile locally
- Everything is ready to go!

---

## 📞 Support

If you encounter issues:
1. Check terminal logs
2. Use the troubleshooting guide
3. Make sure both services are running

**Good luck! 🎉** 
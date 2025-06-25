# 🚀 Quick Start Guide

## The Issue You Encountered

The error occurred because you were running the startup script from the wrong directory. The script needs to be run from the main project directory.

## ✅ Fixed Solution

I've created a new, smarter startup script that automatically finds the correct directories.

## 🎯 How to Run (3 Simple Steps)

### 1. Navigate to the Main Project Directory
```bash
cd /Users/shayanhashemi/Downloads/Docx_to_latex
```
**Important**: Make sure you're in the directory that contains `web_api.py` and `converter.py`

### 2. Install Python Dependencies (if not already done)
```bash
pip install -r requirements_web.txt
```

### 3. Start the Application
```bash
python run_app.py
```

That's it! The new script will:
- ✅ Automatically find the correct directories
- ✅ Start the Flask API on http://localhost:5000
- ✅ Start the Next.js frontend on http://localhost:3000
- ✅ Open your browser automatically

## 🔧 Alternative Options

### Test Flask API Only
If you want to test just the backend:
```bash
python test_api.py
```

### Manual Startup (if you prefer)
```bash
# Terminal 1 - Flask API
cd /Users/shayanhashemi/Downloads/Docx_to_latex
python web_api.py

# Terminal 2 - Next.js Frontend
cd /Users/shayanhashemi/Downloads/Docx_to_latex/docx_to_latex
npm run dev
```

## 🐛 Troubleshooting

### "No such file or directory" Error
- Make sure you're in the correct directory (`/Users/shayanhashemi/Downloads/Docx_to_latex`)
- The directory should contain: `web_api.py`, `converter.py`, `run_app.py`

### Flask API Won't Start
- Check if port 5000 is already in use: `lsof -i :5000`
- Kill any existing process: `kill -9 <PID>`

### Next.js Won't Start
- Delete `node_modules` and reinstall: `rm -rf docx_to_latex/node_modules && cd docx_to_latex && npm install`

## 📂 Directory Structure Check

Your directory should look like this:
```
Docx_to_latex/                    ← Run scripts from here
├── web_api.py                    ← Flask API
├── converter.py                  ← Core converter
├── run_app.py                    ← New startup script
├── test_api.py                   ← API test script
├── requirements_web.txt          ← Python dependencies
└── docx_to_latex/               ← Next.js frontend
    ├── package.json
    ├── src/app/page.tsx
    └── ...
```

## 🎉 Success!

Once running, you'll see:
- Flask API at: http://localhost:5000
- Web Interface at: http://localhost:3000

The beautiful web interface will automatically open in your browser!

---

**Need help?** The new `run_app.py` script has better error messages and will guide you if something goes wrong. 
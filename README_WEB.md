# 🚀 DOCX to LaTeX Web Converter

A modern, beautiful web interface for converting Microsoft Word documents (.docx) to LaTeX format with enhanced features and Overleaf compatibility.

![Web Interface Preview](https://img.shields.io/badge/Interface-Modern%20Web%20UI-blue?style=for-the-badge)
![Backend](https://img.shields.io/badge/Backend-Flask%20API-green?style=for-the-badge)
![Frontend](https://img.shields.io/badge/Frontend-Next.js%20React-black?style=for-the-badge)

## ✨ Features

### 🎨 **Modern Web Interface**
- Beautiful, responsive design with glassmorphism effects
- Animated backgrounds and smooth transitions
- Dark/light theme support
- Drag & drop file upload
- Real-time conversion progress
- Mobile-friendly design

### 🔧 **Enhanced Conversion Options**
- **Overleaf Compatible**: Fixes image paths for cloud LaTeX editors
- **Style Preservation**: Maintains document formatting and centering
- **Line Break Preservation**: Fixes numbered lists and pagination
- **Table of Contents**: Automatic TOC generation
- **Media Extraction**: Extracts and organizes images

### 🌟 **Advanced Features**
- Unicode mathematical character conversion
- Mixed mathematical expression cleanup
- LaTeX compilation error prevention
- Automatic package injection
- File cleanup and management

## 🛠️ Installation & Setup

### Prerequisites

1. **Python 3.8+** with pip
2. **Node.js 18+** with npm
3. **Pandoc** (required for document conversion)

### Quick Start

1. **Clone or navigate to the project directory**
   ```bash
   cd Docx_to_latex
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements_web.txt
   ```

3. **Install Pandoc**
   - **Windows**: Download from [pandoc.org](https://pandoc.org/installing.html)
   - **macOS**: `brew install pandoc`
   - **Linux**: `sudo apt-get install pandoc` or `sudo yum install pandoc`

4. **Start the application**
   ```bash
   python start_web_app.py
   ```

The application will automatically:
- Install Node.js dependencies
- Start the Flask API (http://localhost:5000)
- Start the Next.js frontend (http://localhost:3000)
- Open your web browser

## 🎯 How to Use

### 1. **Upload Document**
- Drag and drop your `.docx` file onto the upload area
- Or click to browse and select your file
- Supported formats: Microsoft Word (.docx)

### 2. **Configure Options**
- **Generate Table of Contents**: Creates automatic TOC
- **Overleaf Compatible**: ✅ Recommended for cloud editors
- **Preserve Styles**: ✅ Maintains formatting and centering
- **Preserve Line Breaks**: ✅ Fixes lists and pagination

### 3. **Set Output Name**
- Modify the output filename if needed
- Default: `your-document.tex`

### 4. **Convert & Download**
- Click "Convert to LaTeX"
- Watch the real-time progress
- Download your converted file when complete

## 🏗️ Architecture

### Backend (Flask API)
```
web_api.py              # Flask REST API server
├── /api/upload         # File upload endpoint
├── /api/convert        # Conversion endpoint
├── /api/download       # File download endpoint
├── /api/status         # Task status checking
└── /api/cleanup        # File cleanup
```

### Frontend (Next.js + React)
```
docx_to_latex/
├── src/app/
│   ├── page.tsx        # Main conversion interface
│   ├── layout.tsx      # App layout
│   └── globals.css     # Global styles
├── public/             # Static assets
└── package.json        # Dependencies
```

### Core Converter
```
converter.py            # Core conversion logic
├── convert_docx_to_latex()
├── _apply_post_processing()
├── _convert_unicode_math_characters()
└── _fix_compilation_issues()
```

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload DOCX file |
| `POST` | `/api/convert` | Start conversion |
| `GET` | `/api/download/<task_id>` | Download LaTeX file |
| `GET` | `/api/download-media/<task_id>` | Download media ZIP |
| `GET` | `/api/status/<task_id>` | Check conversion status |
| `DELETE` | `/api/cleanup/<task_id>` | Clean up files |
| `GET` | `/api/health` | Health check |

## 🎨 UI Features

### Design Elements
- **Glassmorphism**: Frosted glass effects with backdrop blur
- **Gradient Backgrounds**: Dynamic animated blob gradients
- **Smooth Animations**: CSS transitions and keyframe animations
- **Responsive Layout**: Mobile-first design with Tailwind CSS
- **Interactive Elements**: Hover effects and state changes

### User Experience
- **Drag & Drop**: Intuitive file upload
- **Real-time Feedback**: Progress indicators and status updates
- **Error Handling**: Graceful error messages and recovery
- **Accessibility**: Semantic HTML and keyboard navigation

## 🔍 Troubleshooting

### Common Issues

1. **"Pandoc not found" error**
   - Install Pandoc from [pandoc.org](https://pandoc.org/installing.html)
   - Ensure Pandoc is in your system PATH

2. **CORS errors in browser**
   - The Flask API includes CORS support
   - Check that both servers are running on correct ports

3. **File upload fails**
   - Check file size (max 16MB)
   - Ensure file is a valid `.docx` format

4. **Conversion fails**
   - Check the browser console for error details
   - Verify the DOCX file is not corrupted

### Port Configuration

Default ports:
- Flask API: `http://localhost:5000`
- Next.js: `http://localhost:3000`

To change ports, modify:
- Flask: Edit `port=5000` in `web_api.py`
- Next.js: Use `npm run dev -- -p 3001`

## 🚀 Deployment

### Development
```bash
python start_web_app.py
```

### Production (Flask API)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_api:app
```

### Production (Next.js)
```bash
cd docx_to_latex
npm run build
npm start
```

## 📁 File Structure
```
Docx_to_latex/
├── 📄 converter.py           # Core conversion engine
├── 🖥️ app.py                # Original Tkinter GUI
├── 🌐 web_api.py             # Flask REST API
├── 🚀 start_web_app.py       # Startup script
├── 📋 requirements_web.txt   # Python dependencies
├── 📖 README_WEB.md          # This file
└── 📁 docx_to_latex/         # Next.js frontend
    ├── 📁 src/app/
    │   ├── 🎨 page.tsx       # Main UI component
    │   ├── 🏗️ layout.tsx     # App layout
    │   └── 🎨 globals.css    # Global styles
    ├── 📋 package.json       # Node dependencies
    └── ⚙️ next.config.ts     # Next.js config
```

## 💡 Tips for Best Results

1. **Use Enhanced Options**: Keep Overleaf Compatible, Preserve Styles, and Preserve Line Breaks enabled
2. **Document Structure**: Use proper headings (H1, H2, H3) for better LaTeX structure
3. **Images**: Ensure images are embedded properly in your Word document
4. **Mathematical Content**: Use Word's equation editor for best LaTeX math conversion
5. **File Organization**: The converter extracts media to separate folders for better organization

## 🆚 Comparison: Web vs Desktop

| Feature | Web Interface | Desktop (Tkinter) |
|---------|---------------|-------------------|
| **User Experience** | Modern, intuitive | Functional, basic |
| **File Handling** | Drag & drop | File dialogs |
| **Progress Feedback** | Real-time animations | Text status |
| **Multi-platform** | ✅ Any browser | ✅ Cross-platform |
| **Remote Access** | ✅ Web-based | ❌ Local only |
| **Mobile Support** | ✅ Responsive | ❌ Desktop only |

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional LaTeX template support
- Batch conversion capabilities
- Advanced styling options
- Integration with cloud storage
- Real-time collaborative editing

## 📄 License

This project is part of the DOCX to LaTeX Converter suite. Please refer to the main project license.

---

**Built with ❤️ using Flask, React, Next.js, and Tailwind CSS**

*For support or questions, please refer to the main project documentation.* 
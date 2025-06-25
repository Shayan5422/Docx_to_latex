---
title: DOCX to LaTeX Converter
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# 📄 DOCX to LaTeX Converter API

تبدیل‌کننده حرفه‌ای فایل‌های Word (DOCX) به LaTeX با قابلیت‌های پیشرفته

A professional DOCX to LaTeX converter with advanced features and modern web interface.

## 🌟 ویژگی‌ها / Features

### فارسی
- ✅ تبدیل فایل‌های DOCX به LaTeX با کیفیت بالا
- ✅ استخراج و حفظ تصاویر
- ✅ سازگار با Overleaf
- ✅ حفظ فرمت‌ها و استایل‌ها
- ✅ تولید فهرست مطالب خودکار
- ✅ دانلود فایل کامل در قالب ZIP
- ✅ رابط API ساده و قدرتمند
- ✅ اجرا رایگان روی Hugging Face Spaces

### English
- ✅ High-quality DOCX to LaTeX conversion
- ✅ Image extraction and preservation
- ✅ Overleaf compatibility
- ✅ Style and formatting preservation
- ✅ Automatic table of contents generation
- ✅ Complete ZIP package download
- ✅ Simple and powerful API interface
- ✅ Free hosting on Hugging Face Spaces

## 🚀 استفاده / Usage

### API Endpoints

#### 1. Health Check
```bash
GET /api/health
```

#### 2. Upload File
```bash
POST /api/upload
Content-Type: multipart/form-data
Body: file (DOCX file)
```

#### 3. Convert Document
```bash
POST /api/convert
Content-Type: application/json
Body: {
  "task_id": "string",
  "output_filename": "string",
  "options": {
    "generateToc": boolean,
    "extractMedia": boolean,
    "overleafCompatible": boolean,
    "preserveStyles": boolean,
    "preserveLineBreaks": boolean
  }
}
```

#### 4. Download Complete Package
```bash
GET /api/download-complete/{task_id}
```

### مثال استفاده / Example Usage

```python
import requests

# Upload file
with open('document.docx', 'rb') as f:
    response = requests.post('https://YOUR_USERNAME-docx-to-latex.hf.space/api/upload', 
                           files={'file': f})
task_id = response.json()['task_id']

# Convert
convert_response = requests.post('https://YOUR_USERNAME-docx-to-latex.hf.space/api/convert', 
                               json={
                                   'task_id': task_id,
                                   'options': {
                                       'generateToc': True,
                                       'extractMedia': True,
                                       'overleafCompatible': True
                                   }
                               })

# Download complete package
download_response = requests.get(f'https://YOUR_USERNAME-docx-to-latex.hf.space/api/download-complete/{task_id}')
with open('converted_package.zip', 'wb') as f:
    f.write(download_response.content)
```

## 🔧 نصب محلی / Local Installation

```bash
git clone https://github.com/YOUR_USERNAME/docx-to-latex.git
cd docx-to-latex
pip install -r requirements.txt
python app.py
```

## 📚 مستندات / Documentation

این API امکان تبدیل فایل‌های Word به LaTeX با حفظ فرمت‌ها، تصاویر و جداول را فراهم می‌کند. خروجی نهایی شامل فایل LaTeX و پوشه تصاویر در قالب ZIP است که مستقیماً در Overleaf قابل استفاده است.

This API provides seamless conversion from Word documents to LaTeX while preserving formatting, images, and tables. The final output includes the LaTeX file and media folder in a ZIP package ready for use in Overleaf.

## 🤝 مشارکت / Contributing

مشارکت‌ها خوشحال دریافت می‌شوند! لطفاً Issue ایجاد کرده یا Pull Request ارسال کنید.

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 مجوز / License

MIT License - برای جزئیات فایل LICENSE را مشاهده کنید.

MIT License - see LICENSE file for details. 
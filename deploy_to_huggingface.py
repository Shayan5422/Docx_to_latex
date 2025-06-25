#!/usr/bin/env python3
"""
Deploy DOCX to LaTeX Converter to Hugging Face Spaces
این اسکریپت فایل‌های لازم برای deploy کردن روی Hugging Face Spaces را آماده می‌کند
"""

import os
import shutil
import sys

def create_deployment_package():
    """Create a deployment package for Hugging Face Spaces"""
    
    print("🚀 آماده‌سازی فایل‌ها برای Hugging Face Spaces...")
    
    # Required files for Hugging Face Spaces
    required_files = [
        'app.py',
        'web_api.py', 
        'converter.py',
        'requirements.txt',
        'README.md',
        'Dockerfile',
        '.gitignore',
        'preserve_linebreaks.lua'
    ]
    
    # Create deployment directory
    deploy_dir = 'huggingface_deployment'
    
    if os.path.exists(deploy_dir):
        print(f"📁 حذف پوشه قبلی {deploy_dir}...")
        shutil.rmtree(deploy_dir)
    
    os.makedirs(deploy_dir)
    print(f"📁 ایجاد پوشه {deploy_dir}...")
    
    # Copy required files
    for file in required_files:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            print(f"✅ کپی شد: {file}")
        else:
            print(f"❌ فایل پیدا نشد: {file}")
    
    # Create temp directories
    temp_dir = os.path.join(deploy_dir, 'temp')
    os.makedirs(os.path.join(temp_dir, 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, 'outputs'), exist_ok=True)
    print("📁 پوشه‌های temp ایجاد شدند")
    
    # Create deployment instructions
    instructions = """
# راهنمای Deploy کردن روی Hugging Face Spaces

## مرحله ۱: ایجاد Space
1. به https://huggingface.co/spaces بروید
2. "Create new Space" را کلیک کنید
3. نام Space را وارد کنید: docx-to-latex
4. SDK: Python انتخاب کنید
5. "Create Space" را کلیک کنید

## مرحله ۲: آپلود فایل‌ها
تمام فایل‌های این پوشه را به Space آپلود کنید:

### روش ۱: Git
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/docx-to-latex
cd docx-to-latex
cp -r ../huggingface_deployment/* .
git add .
git commit -m "Add DOCX to LaTeX converter API"
git push
```

### روش ۲: Web Interface
فایل‌ها را drag & drop کنید در صفحه Space

## مرحله ۳: تست
پس از deploy، API در آدرس زیر دردسترس خواهد بود:
https://YOUR_USERNAME-docx-to-latex.hf.space/api/health

## فایل‌های کپی شده:
""" + '\n'.join([f"- {file}" for file in required_files if os.path.exists(file)])
    
    with open(os.path.join(deploy_dir, 'DEPLOYMENT_INSTRUCTIONS.txt'), 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"\n✅ آماده‌سازی کامل شد!")
    print(f"📁 تمام فایل‌های لازم در پوشه '{deploy_dir}' آماده است")
    print(f"📖 راهنمای deploy در فایل DEPLOYMENT_INSTRUCTIONS.txt موجود است")
    print(f"\n🌐 حالا می‌توانید این فایل‌ها را روی Hugging Face Spaces آپلود کنید")

if __name__ == "__main__":
    create_deployment_package() 
# 🚀 راهنمای اجرا روی Hugging Face Spaces

این راهنما شما را قدم به قدم با نحوه اجرای بک‌اند DOCX to LaTeX روی Hugging Face Spaces آشنا می‌کند.

## 📋 پیش‌نیازها

1. **حساب کاربری Hugging Face**: اگر ندارید از [اینجا](https://huggingface.co/join) ثبت‌نام کنید
2. **Git نصب شده باشد** روی سیستم شما
3. **فایل‌های پروژه** آماده باشند

## 🔧 مرحله ۱: آماده‌سازی فایل‌ها

فایل‌های زیر باید در پوشه اصلی پروژه موجود باشند:

```
Docx_to_latex/
├── app.py                 # ✅ آماده شده
├── web_api.py            # ✅ موجود
├── converter.py          # ✅ موجود
├── requirements.txt      # ✅ آماده شده
├── README.md            # ✅ آماده شده
├── Dockerfile           # ✅ آماده شده
├── .gitignore           # ✅ آماده شده
└── preserve_linebreaks.lua
```

## 🌐 مرحله ۲: ایجاد Space جدید

1. به [Hugging Face Spaces](https://huggingface.co/spaces) بروید
2. روی **"Create new Space"** کلیک کنید
3. اطلاعات زیر را وارد کنید:
   - **Space name**: `docx-to-latex` (یا نام دلخواه)
   - **License**: MIT
   - **SDK**: Python
   - **Visibility**: Public (یا Private)
4. **"Create Space"** را کلیک کنید

## 📁 مرحله ۳: آپلود فایل‌ها

### روش ۱: استفاده از Git (توصیه شده)

```bash
# Clone کردن repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/docx-to-latex
cd docx-to-latex

# کپی کردن فایل‌های پروژه
cp /Users/shayanhashemi/Downloads/Docx_to_latex/Docx_to_latex/* .

# اضافه کردن فایل‌ها به Git
git add .
git commit -m "Add DOCX to LaTeX converter API"
git push
```

### روش ۲: آپلود مستقیم از وب

1. در صفحه Space خود، روی **"Files"** کلیک کنید
2. **"Add file"** > **"Upload files"** را انتخاب کنید
3. تمام فایل‌های لازم را drag & drop کنید
4. **"Commit changes"** را کلیک کنید

## ⚙️ مرحله ۴: تنظیمات Space

در فایل `README.md` که ایجاد شده، بخش بالایی را با اطلاعات خود تطبیق دهید:

```yaml
---
title: DOCX to LaTeX Converter
emoji: 📄
colorFrom: blue
colorTo: green
sdk: python
sdk_version: 3.9
app_file: app.py
pinned: false
license: mit
---
```

## 🚀 مرحله ۵: راه‌اندازی

1. فایل‌ها آپلود شدن، Space به‌طور خودکار شروع به build می‌کند
2. فرآیند build حدود ۲-۵ دقیقه طول می‌کشد
3. پس از اتمام، API شما در آدرس زیر دردسترس خواهد بود:
   ```
   https://YOUR_USERNAME-docx-to-latex.hf.space
   ```

## 🔍 مرحله ۶: تست API

### Health Check
```bash
curl https://YOUR_USERNAME-docx-to-latex.hf.space/api/health
```

### آپلود و تبدیل فایل
```python
import requests

# آپلود فایل
url = "https://YOUR_USERNAME-docx-to-latex.hf.space"
with open('test.docx', 'rb') as f:
    response = requests.post(f'{url}/api/upload', files={'file': f})
    task_id = response.json()['task_id']

# تبدیل
convert_response = requests.post(f'{url}/api/convert', json={
    'task_id': task_id,
    'options': {
        'generateToc': True,
        'extractMedia': True,
        'overleafCompatible': True
    }
})

# دانلود
download_response = requests.get(f'{url}/api/download-complete/{task_id}')
with open('result.zip', 'wb') as f:
    f.write(download_response.content)
```

## 🔧 تنظیمات پیشرفته

### افزایش Memory و CPU
اگر فایل‌های بزرگ دارید، می‌توانید Space را upgrade کنید:

1. در صفحه Space، روی **"Settings"** کلیک کنید
2. **"Hardware"** را انتخاب کنید
3. پلن مناسب را انتخاب کنید (CPU basic رایگان است)

### متغیرهای محیطی
در بخش Settings > Variables می‌توانید متغیرهای محیطی اضافه کنید:

```
MAX_FILE_SIZE=50MB
DEBUG=false
```

## 🔒 امنیت

### Private Space
برای استفاده خصوصی:
1. Settings > Visibility > Private

### محدودیت دسترسی
می‌توانید IP های مجاز یا authentication اضافه کنید.

## 📊 مانیتورینگ

### لاگ‌ها
- **Logs** tab: مشاهده real-time logs
- **Community** tab: کامنت‌ها و بازخوردها

### آمار استفاده
در داشبورد Space می‌توانید آمار استفاده را مشاهده کنید.

## 🔄 به‌روزرسانی

برای به‌روزرسانی کد:

```bash
# تغییرات را commit کنید
git add .
git commit -m "Update API features"
git push
```

Space به‌طور خودکار rebuild خواهد شد.

## 🆘 عیب‌یابی

### مشکلات رایج

1. **Build Failed**: 
   - بررسی کنید requirements.txt درست باشد
   - لاگ‌های build را چک کنید

2. **Memory Error**:
   - فایل‌های بزرگ را محدود کنید
   - Hardware upgrade کنید

3. **Timeout**:
   - فرآیند conversion را بهینه کنید
   - Cache اضافه کنید

### لاگ‌های مفید
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/convert', methods=['POST'])
def convert_document():
    logger.info(f"Converting task: {task_id}")
    # ... conversion code
```

## 🎯 نکات بهینه‌سازی

1. **Caching**: فایل‌های تبدیل شده را cache کنید
2. **Async Processing**: برای فایل‌های بزرگ از background jobs استفاده کنید
3. **Error Handling**: پیام‌های خطای واضح ارائه دهید
4. **Rate Limiting**: محدودیت تعداد درخواست اضافه کنید

## 📞 پشتیبانی

- [Hugging Face Community](https://huggingface.co/spaces/YOUR_USERNAME/docx-to-latex/community)
- [Documentation](https://huggingface.co/docs/hub/spaces)
- [Discord](https://discord.gg/hugging-face)

---

✅ **تبریک!** حالا API شما روی Hugging Face Spaces در دسترس جهانی است!

🔗 **لینک Space شما**: `https://YOUR_USERNAME-docx-to-latex.hf.space` 
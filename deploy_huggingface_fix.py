#!/usr/bin/env python3
"""
Deploy updated files to Hugging Face Spaces to fix permission issues
"""

import os
import shutil
from huggingface_hub import HfApi, upload_file

def deploy_to_huggingface():
    """Deploy the updated files to fix the permission issue"""
    
    # Your Hugging Face Space repository
    repo_id = "shayan5422/Docx_to_latex"
    repo_type = "space"
    
    print("🚀 Deploying permission fixes to Hugging Face Spaces...")
    print(f"📍 Repository: {repo_id}")
    
    try:
        api = HfApi()
        
        # Files to upload with their paths
        files_to_upload = [
            ("huggingface_deployment/app.py", "app.py"),
            ("huggingface_deployment/web_api.py", "web_api.py"), 
            ("huggingface_deployment/Dockerfile", "Dockerfile"),
            ("huggingface_deployment/converter.py", "converter.py"),
            ("huggingface_deployment/requirements.txt", "requirements.txt"),
            ("huggingface_deployment/preserve_linebreaks.lua", "preserve_linebreaks.lua"),
        ]
        
        for local_path, remote_path in files_to_upload:
            if os.path.exists(local_path):
                print(f"📤 Uploading {local_path} -> {remote_path}")
                try:
                    upload_file(
                        path_or_fileobj=local_path,
                        path_in_repo=remote_path,
                        repo_id=repo_id,
                        repo_type=repo_type,
                        commit_message=f"Fix file permission issues - Update {remote_path}"
                    )
                    print(f"   ✅ {remote_path} uploaded successfully")
                except Exception as e:
                    print(f"   ❌ Failed to upload {remote_path}: {e}")
            else:
                print(f"   ⚠️ File not found: {local_path}")
        
        print("\n🎉 Deployment completed!")
        print("📍 Your Space: https://huggingface.co/spaces/shayan5422/Docx_to_latex")
        print("⏳ The Space will rebuild automatically (may take a few minutes)")
        print("\n💡 Changes made:")
        print("   • Fixed file permission issues")
        print("   • Using system temporary directories")
        print("   • Improved error handling")
        print("   • Better cleanup on exit")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    success = deploy_to_huggingface()
    if success:
        print("\n✨ Next steps:")
        print("1. Wait for Space rebuild (check status on HF)")
        print("2. Test the upload functionality")
        print("3. Enjoy the fixed permission issues!")
    else:
        print("\n🔧 Manual deployment option:")
        print("1. Visit https://huggingface.co/spaces/shayan5422/Docx_to_latex")
        print("2. Upload the files from huggingface_deployment/ folder")
        print("3. The Space will rebuild automatically") 
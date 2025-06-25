#!/usr/bin/env python3
"""
Backend startup script for DOCX to LaTeX API
Separate Flask API server launcher
"""

import subprocess
import sys
import os
from pathlib import Path

def find_project_root():
    """Find the project root directory"""
    current = Path.cwd()
    
    # بررسی پوشه فعلی
    if (current / 'web_api.py').exists() and (current / 'converter.py').exists():
        return current
    
    # بررسی پوشه والد
    parent = current.parent
    if (parent / 'web_api.py').exists() and (parent / 'converter.py').exists():
        return parent
    
    # جستجو در پوشه‌های بالاتر
    for parent_dir in current.parents:
        if (parent_dir / 'web_api.py').exists() and (parent_dir / 'converter.py').exists():
            return parent_dir
    
    return None

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['flask', 'flask_cors', 'pypandoc']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print("pip install -r requirements_web.txt")
        return False
    
    return True

def main():
    """Main backend startup function"""
    print("=" * 60)
    print("🚀 DOCX to LaTeX - Backend API Server")
    print("=" * 60)
    
    # Find project root
    project_root = find_project_root()
    if not project_root:
        print("❌ Error: Could not find project root directory!")
        print("Please make sure you're running this from the project directory.")
        sys.exit(1)
    
    print(f"✅ Project root: {project_root}")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Change to project directory
    original_dir = os.getcwd()
    os.chdir(project_root)
    
    try:
        print("\n🔧 Starting backend server...")
        print("- API Server: http://localhost:5000")
        print("- Health Check: http://localhost:5000/api/health")
        print("\nPress Ctrl+C to stop\n")
        
        # Run Flask API
        subprocess.run([sys.executable, 'web_api.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")
    except Exception as e:
        print(f"❌ Error running backend: {e}")
    finally:
        os.chdir(original_dir)

if __name__ == '__main__':
    main() 
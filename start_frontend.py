#!/usr/bin/env python3
"""
Frontend startup script for DOCX to LaTeX Web Interface
Separate Next.js development server launcher
"""

import subprocess
import sys
import os
import time
import webbrowser
import threading
from pathlib import Path

def find_frontend_dir():
    """Find the Next.js frontend directory"""
    current = Path.cwd()
    
    # بررسی پوشه docx_to_latex در دایرکتوری فعلی
    frontend_dir = current / 'docx_to_latex'
    if frontend_dir.exists() and (frontend_dir / 'package.json').exists():
        return frontend_dir
    
    # بررسی پوشه والد
    parent = current.parent
    frontend_dir = parent / 'docx_to_latex'
    if frontend_dir.exists() and (frontend_dir / 'package.json').exists():
        return frontend_dir
    
    # اگر در پوشه فرانت‌اند هستیم
    if (current / 'package.json').exists() and (current / 'next.config.ts').exists():
        return current
    
    return None

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js installed: {version}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ Node.js not found!")
    print("Please install Node.js from: https://nodejs.org/")
    return False

def open_browser():
    """Open web browser after a delay"""
    time.sleep(3)  # Wait for server to start
    try:
        # Try ports 3000, then 3001, then 3002
        for port in [3000, 3001, 3002]:
            try:
                webbrowser.open(f'http://localhost:{port}')
                print(f"🌐 Browser opened: http://localhost:{port}")
                break
            except Exception:
                continue
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print("Please open http://localhost:3000 in your browser")

def main():
    """Main frontend startup function"""
    print("=" * 60)
    print("🎨 DOCX to LaTeX - Frontend Web Interface")
    print("=" * 60)
    
    # Check Node.js
    if not check_node():
        sys.exit(1)
    
    # Find frontend directory
    frontend_dir = find_frontend_dir()
    if not frontend_dir:
        print("❌ Error: Could not find Next.js frontend directory!")
        print("Looking for 'docx_to_latex' directory with package.json")
        sys.exit(1)
    
    print(f"✅ Frontend directory: {frontend_dir}")
    
    # Change to frontend directory
    original_dir = os.getcwd()
    os.chdir(frontend_dir)
    
    try:
        print("\n🔧 Starting frontend server...")
        print("- Web Interface: http://localhost:3000")
        print("- Make sure backend is running on port 5000")
        print("\nPress Ctrl+C to stop\n")
        
        # Check node_modules and install dependencies
        if not (frontend_dir / 'node_modules').exists():
            print("📦 Installing Node.js dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        # Open browser in separate thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Run Next.js server
        subprocess.run(['npm', 'run', 'dev'], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    except Exception as e:
        print(f"❌ Error running frontend: {e}")
        if "npm" in str(e):
            print("Please install npm and Node.js")
    finally:
        os.chdir(original_dir)

if __name__ == '__main__':
    main() 
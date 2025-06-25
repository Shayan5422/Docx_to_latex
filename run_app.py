#!/usr/bin/env python3
"""
Simple startup script for DOCX to LaTeX Web Application
This script automatically finds the correct directories and starts both services.
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def find_project_root():
    """Find the project root directory containing web_api.py and converter.py"""
    current = Path.cwd()
    
    # Check current directory first
    if (current / 'web_api.py').exists() and (current / 'converter.py').exists():
        return current
    
    # Check parent directory
    parent = current.parent
    if (parent / 'web_api.py').exists() and (parent / 'converter.py').exists():
        return parent
    
    # Search up the directory tree
    for parent_dir in current.parents:
        if (parent_dir / 'web_api.py').exists() and (parent_dir / 'converter.py').exists():
            return parent_dir
    
    return None

def find_frontend_dir(project_root):
    """Find the Next.js frontend directory"""
    # Look for docx_to_latex directory with package.json
    frontend_dir = project_root / 'docx_to_latex'
    if frontend_dir.exists() and (frontend_dir / 'package.json').exists():
        return frontend_dir
    
    # If current directory is the frontend directory
    if (Path.cwd() / 'package.json').exists() and (Path.cwd() / 'next.config.ts').exists():
        return Path.cwd()
    
    return None

def run_flask_api(project_root):
    """Run the Flask API server"""
    print("🚀 Starting Flask API server...")
    original_dir = os.getcwd()
    try:
        os.chdir(project_root)
        subprocess.run([sys.executable, 'web_api.py'], check=True)
    except KeyboardInterrupt:
        print("Flask API server stopped")
    except Exception as e:
        print(f"❌ Error running Flask API: {e}")
    finally:
        os.chdir(original_dir)

def run_nextjs_frontend(frontend_dir):
    """Run the Next.js frontend"""
    print("🎨 Starting Next.js frontend...")
    original_dir = os.getcwd()
    try:
        os.chdir(frontend_dir)
        
        # Check if node_modules exists, if not run npm install
        if not (frontend_dir / 'node_modules').exists():
            print("📦 Installing Node.js dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        # Start the development server
        subprocess.run(['npm', 'run', 'dev'], check=True)
    except KeyboardInterrupt:
        print("Next.js frontend stopped")
    except Exception as e:
        print(f"❌ Error running Next.js frontend: {e}")
    finally:
        os.chdir(original_dir)

def open_browser():
    """Open the web browser after a delay"""
    time.sleep(3)  # Wait for servers to start
    try:
        webbrowser.open('http://localhost:3000')
        print("🌐 Opening web browser at http://localhost:3000")
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print("Please open http://localhost:3000 in your browser")

def main():
    """Main startup function"""
    print("=" * 60)
    print("🚀 DOCX to LaTeX Web Application")
    print("=" * 60)
    
    # Find project directories
    project_root = find_project_root()
    if not project_root:
        print("❌ Error: Could not find project root directory!")
        print("Please make sure you're running this from the project directory.")
        sys.exit(1)
    
    frontend_dir = find_frontend_dir(project_root)
    if not frontend_dir:
        print("❌ Error: Could not find Next.js frontend directory!")
        print(f"Looked for 'docx_to_latex' directory in: {project_root}")
        sys.exit(1)
    
    print(f"✅ Project root: {project_root}")
    print(f"✅ Frontend directory: {frontend_dir}")
    
    print("\n🔧 Starting services...")
    print("- Flask API will run on: http://localhost:5000")
    print("- Next.js frontend will run on: http://localhost:3000")
    print("\nPress Ctrl+C to stop all services\n")
    
    try:
        # Start Flask API in a separate thread
        flask_thread = threading.Thread(target=run_flask_api, args=(project_root,), daemon=True)
        flask_thread.start()
        
        # Wait a moment for Flask to start
        time.sleep(2)
        
        # Open browser in a separate thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Run Next.js frontend in the main thread
        run_nextjs_frontend(frontend_dir)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down all services...")
        print("Thank you for using DOCX to LaTeX Converter!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 
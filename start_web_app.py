#!/usr/bin/env python3
"""
Startup script for the DOCX to LaTeX Web Application
This script runs both the Flask API backend and Next.js frontend
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

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
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print("pip install -r requirements_web.txt")
        return False
    
    return True

def check_pandoc():
    """Check if Pandoc is installed"""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ Pandoc is installed")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("⚠ Pandoc is not installed or not in PATH")
    print("Please install Pandoc from: https://pandoc.org/installing.html")
    return False

def run_flask_api():
    """Run the Flask API server"""
    print("Starting Flask API server...")
    try:
        # Find the web_api.py file
        current_dir = Path.cwd()
        web_api_path = current_dir / 'web_api.py'
        
        if not web_api_path.exists():
            # Try parent directory
            parent_dir = current_dir.parent
            web_api_path = parent_dir / 'web_api.py'
            if web_api_path.exists():
                os.chdir(parent_dir)
        
        if not web_api_path.exists():
            print("Error: web_api.py not found!")
            return
            
        subprocess.run([sys.executable, 'web_api.py'], check=True)
    except KeyboardInterrupt:
        print("Flask API server stopped")
    except Exception as e:
        print(f"Error running Flask API: {e}")

def run_nextjs_frontend():
    """Run the Next.js frontend"""
    print("Starting Next.js frontend...")
    
    # Find the Next.js frontend directory
    current_dir = Path.cwd()
    frontend_dir = current_dir / 'docx_to_latex'
    
    if not frontend_dir.exists():
        # Try parent directory
        parent_dir = current_dir.parent
        frontend_dir = parent_dir / 'docx_to_latex'
        if not frontend_dir.exists():
            # Try current directory if we're already in docx_to_latex
            if current_dir.name == 'docx_to_latex' and (current_dir / 'package.json').exists():
                frontend_dir = current_dir
            else:
                print("Error: Next.js frontend directory not found!")
                print(f"Looked in: {current_dir / 'docx_to_latex'}")
                print(f"Also looked in: {parent_dir / 'docx_to_latex'}")
                return
    
    os.chdir(frontend_dir)
    
    try:
        # Check if node_modules exists, if not run npm install
        if not Path('node_modules').exists():
            print("Installing Node.js dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        # Start the development server
        subprocess.run(['npm', 'run', 'dev'], check=True)
    except KeyboardInterrupt:
        print("Next.js frontend stopped")
    except Exception as e:
        print(f"Error running Next.js frontend: {e}")

def open_browser():
    """Open the web browser after a delay"""
    time.sleep(3)  # Wait for servers to start
    try:
        webbrowser.open('http://localhost:3000')
        print("Opening web browser at http://localhost:3000")
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print("Please open http://localhost:3000 in your browser")

def main():
    """Main startup function"""
    print("=" * 60)
    print("DOCX to LaTeX Web Application Startup")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check Pandoc (warning only)
    check_pandoc()
    
    print("\nStarting services...")
    print("- Flask API will run on: http://localhost:5000")
    print("- Next.js frontend will run on: http://localhost:3000")
    print("\nPress Ctrl+C to stop all services\n")
    
    try:
        # Start Flask API in a separate thread
        flask_thread = threading.Thread(target=run_flask_api, daemon=True)
        flask_thread.start()
        
        # Wait a moment for Flask to start
        time.sleep(2)
        
        # Open browser in a separate thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Run Next.js frontend in the main thread
        run_nextjs_frontend()
        
    except KeyboardInterrupt:
        print("\n\nShutting down all services...")
        print("Thank you for using DOCX to LaTeX Converter!")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 
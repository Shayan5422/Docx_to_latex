#!/usr/bin/env python3
"""
Test script to run just the Flask API for debugging
"""

import subprocess
import sys
import os
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

def main():
    """Main function to test Flask API"""
    print("🧪 Testing Flask API only...")
    
    # Find project root
    project_root = find_project_root()
    if not project_root:
        print("❌ Error: Could not find project root directory!")
        print("Please make sure you're running this from the project directory.")
        sys.exit(1)
    
    print(f"✅ Project root: {project_root}")
    
    # Change to project root
    original_dir = os.getcwd()
    os.chdir(project_root)
    
    try:
        print("🚀 Starting Flask API on http://localhost:5000")
        print("Press Ctrl+C to stop\n")
        subprocess.run([sys.executable, 'web_api.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Flask API stopped")
    except Exception as e:
        print(f"❌ Error running Flask API: {e}")
    finally:
        os.chdir(original_dir)

if __name__ == '__main__':
    main() 
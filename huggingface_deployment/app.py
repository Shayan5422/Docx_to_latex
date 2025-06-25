#!/usr/bin/env python3
"""
DOCX to LaTeX Converter API
Main entry point for Hugging Face Spaces deployment with improved file handling
"""

import os
import sys
import tempfile

# Set up environment for Hugging Face Spaces
if 'SPACE_ID' in os.environ:
    # Running on Hugging Face Spaces
    PORT = int(os.environ.get('PORT', 7860))
    HOST = '0.0.0.0'
    
    # Ensure we have a writable temp directory
    temp_dir = os.environ.get('TMPDIR', tempfile.gettempdir())
    print(f"📁 Using temp directory: {temp_dir}")
    
    # Test write permissions
    try:
        test_file = os.path.join(temp_dir, 'test_write.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.unlink(test_file)
        print("✅ Write permissions confirmed")
    except Exception as e:
        print(f"⚠️ Write permission test failed: {e}")
else:
    # Running locally
    PORT = 5001
    HOST = '127.0.0.1'

# Import the Flask app
from web_api import app

if __name__ == "__main__":
    print(f"🚀 Starting DOCX to LaTeX Converter API")
    print(f"🌐 Server running on http://{HOST}:{PORT}")
    print(f"📖 Health check: http://{HOST}:{PORT}/api/health")
    print(f"📚 API Documentation: https://huggingface.co/spaces/shayan5422/Docx_to_latex")
    
    # Enable proper error handling for file operations
    try:
        app.run(
            host=HOST,
            port=PORT,
            debug=False  # Disable debug in production
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1) 
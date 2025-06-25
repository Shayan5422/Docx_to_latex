#!/usr/bin/env python3
"""
DOCX to LaTeX Converter API
Main entry point for Hugging Face Spaces deployment
"""

import os
import sys

# Set up environment for Hugging Face Spaces
if 'SPACE_ID' in os.environ:
    # Running on Hugging Face Spaces
    PORT = int(os.environ.get('PORT', 7860))
    HOST = '0.0.0.0'
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
    print(f"📚 API Documentation: https://huggingface.co/spaces/YOUR_USERNAME/docx-to-latex")
    
    app.run(
        host=HOST,
        port=PORT,
        debug=False  # Disable debug in production
    ) 
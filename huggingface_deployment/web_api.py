from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import uuid
from werkzeug.utils import secure_filename
from converter import convert_docx_to_latex
import shutil
import stat

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Use system temp directory for better compatibility with Hugging Face Spaces
TEMP_BASE_DIR = tempfile.mkdtemp(prefix='docx_converter_')
UPLOAD_FOLDER = os.path.join(TEMP_BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(TEMP_BASE_DIR, 'outputs')

# Ensure directories exist with proper permissions
def create_temp_dirs():
    """Create temporary directories with proper permissions"""
    for directory in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        os.makedirs(directory, exist_ok=True)
        # Set full permissions for the directory
        try:
            os.chmod(directory, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        except OSError:
            # If chmod fails, continue anyway (some systems don't allow it)
            pass

# Create directories on startup
create_temp_dirs()

# Store conversion tasks
conversion_tasks = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'DOCX to LaTeX API is running',
        'temp_dir': TEMP_BASE_DIR,
        'upload_dir': UPLOAD_FOLDER,
        'output_dir': OUTPUT_FOLDER
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.docx'):
            return jsonify({'error': 'Only DOCX files are allowed'}), 400
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Save uploaded file using tempfile for better compatibility
        filename = secure_filename(file.filename)
        
        # Create a temporary file instead of using a fixed path
        temp_fd, temp_path = tempfile.mkstemp(
            suffix=f'_{filename}', 
            prefix=f'{task_id}_',
            dir=UPLOAD_FOLDER
        )
        
        try:
            # Close the file descriptor and save the file
            os.close(temp_fd)
            file.save(temp_path)
            
            # Set proper permissions on the file
            try:
                os.chmod(temp_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)
            except OSError:
                # If chmod fails, continue anyway
                pass
            
            # Store task info
            conversion_tasks[task_id] = {
                'status': 'uploaded',
                'original_filename': filename,
                'file_path': temp_path,
                'output_filename': filename.replace('.docx', '.tex'),
                'created_at': os.path.getctime(temp_path)
            }
            
            return jsonify({
                'task_id': task_id,
                'filename': filename,
                'status': 'uploaded',
                'message': 'File uploaded successfully'
            })
            
        except Exception as e:
            # Clean up the temp file if something goes wrong
            try:
                os.unlink(temp_path)
            except:
                pass
            raise e
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/convert', methods=['POST'])
def convert_document():
    """Convert DOCX to LaTeX"""
    try:
        data = request.get_json()
        
        if not data or 'task_id' not in data:
            return jsonify({'error': 'Task ID is required'}), 400
        
        task_id = data['task_id']
        
        if task_id not in conversion_tasks:
            return jsonify({'error': 'Invalid task ID'}), 404
        
        task = conversion_tasks[task_id]
        
        if task['status'] != 'uploaded':
            return jsonify({'error': 'Task is not in uploadable state'}), 400
        
        # Get conversion options
        options = data.get('options', {})
        output_filename = data.get('output_filename', task['output_filename'])
        
        # Update task status
        task['status'] = 'converting'
        task['output_filename'] = output_filename
        
        # Prepare output paths using tempfile for better compatibility
        output_fd, output_path = tempfile.mkstemp(
            suffix=f'_{output_filename}',
            prefix=f'{task_id}_',
            dir=OUTPUT_FOLDER
        )
        os.close(output_fd)  # Close file descriptor, we'll write to the path directly
        
        media_path = tempfile.mkdtemp(
            prefix=f'{task_id}_media_',
            dir=OUTPUT_FOLDER
        )
        
        # Perform conversion
        success, message = convert_docx_to_latex(
            docx_path=task['file_path'],
            latex_path=output_path,
            generate_toc=options.get('generateToc', False),
            extract_media_to_path=media_path if options.get('extractMedia', True) else None,
            latex_template_path=None,  # Could be added later for custom templates
            overleaf_compatible=options.get('overleafCompatible', True),
            preserve_styles=options.get('preserveStyles', True),
            preserve_linebreaks=options.get('preserveLineBreaks', True)
        )
        
        if success:
            task['status'] = 'completed'
            task['output_path'] = output_path
            task['media_path'] = media_path if os.path.exists(media_path) else None
            task['conversion_message'] = message
            
            return jsonify({
                'task_id': task_id,
                'status': 'completed',
                'message': message,
                'output_filename': output_filename,
                'has_media': os.path.exists(media_path)
            })
        else:
            task['status'] = 'failed'
            task['error_message'] = message
            
            return jsonify({
                'task_id': task_id,
                'status': 'failed',
                'error': message
            }), 500
            
    except Exception as e:
        # Update task status if possible
        if 'task_id' in locals() and task_id in conversion_tasks:
            conversion_tasks[task_id]['status'] = 'failed'
            conversion_tasks[task_id]['error_message'] = str(e)
        
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/api/download/<task_id>', methods=['GET'])
def download_file(task_id):
    """Download converted LaTeX file"""
    try:
        if task_id not in conversion_tasks:
            return jsonify({'error': 'Invalid task ID'}), 404
        
        task = conversion_tasks[task_id]
        
        if task['status'] != 'completed':
            return jsonify({'error': 'Conversion not completed'}), 400
        
        if not os.path.exists(task['output_path']):
            return jsonify({'error': 'Output file not found'}), 404
        
        return send_file(
            task['output_path'],
            as_attachment=True,
            download_name=task['output_filename'],
            mimetype='text/plain'
        )
        
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/api/download-media/<task_id>', methods=['GET'])
def download_media(task_id):
    """Download media files as a ZIP archive"""
    try:
        if task_id not in conversion_tasks:
            return jsonify({'error': 'Invalid task ID'}), 404
        
        task = conversion_tasks[task_id]
        
        if task['status'] != 'completed':
            return jsonify({'error': 'Conversion not completed'}), 400
        
        if not task.get('media_path') or not os.path.exists(task['media_path']):
            return jsonify({'error': 'No media files found'}), 404
        
        # Create a ZIP file of the media directory
        zip_path = task['media_path'] + '.zip'
        shutil.make_archive(task['media_path'], 'zip', task['media_path'])
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"{task['output_filename'].replace('.tex', '')}_media.zip",
            mimetype='application/zip'
        )
        
    except Exception as e:
        return jsonify({'error': f'Media download failed: {str(e)}'}), 500

@app.route('/api/download-complete/<task_id>', methods=['GET'])
def download_complete_package(task_id):
    """Download complete package (LaTeX + media) as a ZIP archive"""
    try:
        if task_id not in conversion_tasks:
            return jsonify({'error': 'Invalid task ID'}), 404
        
        task = conversion_tasks[task_id]
        
        if task['status'] != 'completed':
            return jsonify({'error': 'Conversion not completed'}), 400
        
        if not os.path.exists(task['output_path']):
            return jsonify({'error': 'Output file not found'}), 404
        
        # Create a temporary directory for the complete package
        import tempfile
        base_name = task['output_filename'].replace('.tex', '')
        
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = os.path.join(temp_dir, base_name)
            os.makedirs(package_dir, exist_ok=True)
            
            # Copy and fix LaTeX file for Overleaf compatibility
            latex_dest = os.path.join(package_dir, task['output_filename'])
            
            # Read the original LaTeX file
            with open(task['output_path'], 'r', encoding='utf-8') as f:
                latex_content = f.read()
            
            # Fix image paths to use relative paths suitable for Overleaf
            # Convert paths like: task_id_media/media/image.png -> media/image.png
            import re
            
            # Fix paths with task IDs
            latex_content = re.sub(
                r'\\includegraphics(\[[^\]]*\])?\{[^{}]*[a-f0-9\-]+_media[/\\]media[/\\]([^{}]+)\}',
                r'\\includegraphics\1{media/\2}',
                latex_content
            )
            
            # Fix any remaining absolute paths
            latex_content = re.sub(
                r'\\includegraphics(\[[^\]]*\])?\{[^{}]*[/\\]media[/\\]([^{}]+)\}',
                r'\\includegraphics\1{media/\2}',
                latex_content
            )
            
            # Write the fixed LaTeX file
            with open(latex_dest, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Copy media files if they exist
            if task.get('media_path') and os.path.exists(task['media_path']):
                media_dest = os.path.join(package_dir, 'media')
                
                # Check if there's a nested media folder structure
                inner_media = os.path.join(task['media_path'], 'media')
                if os.path.exists(inner_media):
                    # Copy from the inner media folder to avoid media/media/ nesting
                    shutil.copytree(inner_media, media_dest)
                else:
                    # Copy the media_path directly if no nesting
                    shutil.copytree(task['media_path'], media_dest)
            
            # Create README file
            readme_content = f"""# {base_name} - DOCX to LaTeX Conversion

## Package Contents:

1. **{task['output_filename']}** - Main LaTeX file
2. **media/** - Images and media files (if any)

## How to Use:

### Compiling LaTeX:
```bash
pdflatex {task['output_filename']}
```

### For Overleaf:
1. Upload all files to a new Overleaf project
2. Set main file: {task['output_filename']}
3. Compile the project

### Local Compilation:
```bash
# Basic compilation
pdflatex {task['output_filename']}

# For bibliography and cross-references
pdflatex {task['output_filename']}
bibtex {task['output_filename'].replace('.tex', '')}
pdflatex {task['output_filename']}
pdflatex {task['output_filename']}
```

## Features:
- Enhanced formatting preservation
- Overleaf compatibility
- Automatic image path fixing
- Unicode character conversion
- Mathematical expression optimization

## Generated by:
DOCX to LaTeX Web Converter
https://github.com/your-username/docx-to-latex
"""
            
            readme_path = os.path.join(package_dir, 'README.txt')
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # Create ZIP file
            zip_path = os.path.join(temp_dir, f"{base_name}_complete.zip")
            shutil.make_archive(zip_path.replace('.zip', ''), 'zip', package_dir)
            
            return send_file(
                zip_path,
                as_attachment=True,
                download_name=f"{base_name}_complete.zip",
                mimetype='application/zip'
            )
        
    except Exception as e:
        return jsonify({'error': f'Complete package download failed: {str(e)}'}), 500

@app.route('/api/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Get conversion task status"""
    try:
        if task_id not in conversion_tasks:
            return jsonify({'error': 'Invalid task ID'}), 404
        
        task = conversion_tasks[task_id]
        
        response_data = {
            'task_id': task_id,
            'status': task['status'],
            'original_filename': task['original_filename'],
            'output_filename': task.get('output_filename', ''),
        }
        
        if task['status'] == 'completed':
            response_data['message'] = task.get('conversion_message', 'Conversion completed successfully')
            response_data['has_media'] = task.get('media_path') and os.path.exists(task['media_path'])
        elif task['status'] == 'failed':
            response_data['error'] = task.get('error_message', 'Conversion failed')
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'Status check failed: {str(e)}'}), 500

@app.route('/api/cleanup/<task_id>', methods=['DELETE'])
def cleanup_task(task_id):
    """Clean up task files"""
    try:
        if task_id not in conversion_tasks:
            return jsonify({'error': 'Invalid task ID'}), 404
        
        task = conversion_tasks[task_id]
        
        # Remove uploaded file
        if os.path.exists(task['file_path']):
            os.remove(task['file_path'])
        
        # Remove output file
        if task.get('output_path') and os.path.exists(task['output_path']):
            os.remove(task['output_path'])
        
        # Remove media directory
        if task.get('media_path') and os.path.exists(task['media_path']):
            shutil.rmtree(task['media_path'])
        
        # Remove media ZIP if it exists
        media_zip = task.get('media_path', '') + '.zip'
        if os.path.exists(media_zip):
            os.remove(media_zip)
        
        # Remove task from memory
        del conversion_tasks[task_id]
        
        return jsonify({'message': 'Task cleaned up successfully'})
        
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """List all conversion tasks (for debugging)"""
    try:
        tasks_summary = {}
        for task_id, task in conversion_tasks.items():
            tasks_summary[task_id] = {
                'status': task['status'],
                'original_filename': task['original_filename'],
                'output_filename': task.get('output_filename', ''),
                'created_at': task.get('created_at', 0)
            }
        
        return jsonify(tasks_summary)
        
    except Exception as e:
        return jsonify({'error': f'Failed to list tasks: {str(e)}'}), 500

# Cleanup old files on startup
def cleanup_old_files():
    """Remove old temporary files"""
    try:
        import time
        current_time = time.time()
        cutoff_time = current_time - (24 * 60 * 60)  # 24 hours ago
        
        for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path):
                        file_time = os.path.getctime(file_path)
                        if file_time < cutoff_time:
                            os.remove(file_path)
                    elif os.path.isdir(file_path):
                        dir_time = os.path.getctime(file_path)
                        if dir_time < cutoff_time:
                            shutil.rmtree(file_path)
    except Exception as e:
        print(f"Warning: Failed to cleanup old files: {e}")

# Add cleanup on application exit
import atexit

def cleanup_on_exit():
    """Clean up temporary directory on exit"""
    try:
        shutil.rmtree(TEMP_BASE_DIR)
        print(f"Cleaned up temporary directory: {TEMP_BASE_DIR}")
    except OSError:
        pass

atexit.register(cleanup_on_exit)

if __name__ == '__main__':
    # Cleanup old files on startup
    cleanup_old_files()
    
    # Run the Flask app
    print("Starting DOCX to LaTeX API server...")
    print(f"Using temporary directory: {TEMP_BASE_DIR}")
    print("API endpoints:")
    print("  POST /api/upload - Upload DOCX file")
    print("  POST /api/convert - Convert to LaTeX")
    print("  GET /api/download/<task_id> - Download LaTeX file")
    print("  GET /api/download-media/<task_id> - Download media files")
    print("  GET /api/status/<task_id> - Get conversion status")
    print("  DELETE /api/cleanup/<task_id> - Cleanup task files")
    print("  GET /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 
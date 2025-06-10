import pypandoc
import os
import re
import tempfile

def convert_docx_to_latex(
    docx_path: str,
    latex_path: str,
    generate_toc: bool = False,
    extract_media_to_path: str = None,
    latex_template_path: str = None,
    overleaf_compatible: bool = False,
    preserve_styles: bool = True,
    preserve_linebreaks: bool = True
) -> tuple[bool, str]:
    """
    Converts a DOCX file to a LaTeX file using pypandoc with enhanced features.

    Args:
        docx_path: Path to the input .docx file.
        latex_path: Path to save the output .tex file.
        generate_toc: If True, attempts to generate a Table of Contents.
        extract_media_to_path: If specified, path to extract media to (e.g., "./media").
        latex_template_path: If specified, path to a custom Pandoc LaTeX template file.
        overleaf_compatible: If True, makes images work in Overleaf with relative paths.
        preserve_styles: If True, preserves document styles like centering and alignment.
        preserve_linebreaks: If True, preserves line breaks and proper list formatting.

    Returns:
        A tuple (success: bool, message: str).
    """
    extra_args = []
    
    # Ensure standalone document (not fragment)
    extra_args.append("--standalone")
    
    # Basic options
    if generate_toc:
        extra_args.append("--toc")
    if extract_media_to_path:
        extra_args.append(f"--extract-media={extract_media_to_path}")
    if latex_template_path and os.path.isfile(latex_template_path):
        extra_args.append(f"--template={latex_template_path}")
    elif latex_template_path:
        pass  # Template not found, Pandoc will handle the error

    # Enhanced features
    if overleaf_compatible:
        extra_args.extend([
            "--resource-path=./",
            "--default-image-extension=png"
        ])
    
    if preserve_styles:
        extra_args.extend([
            "--from=docx+styles",
            "--wrap=preserve",
            "--columns=72"
        ])
    
    if preserve_linebreaks:
        extra_args.append("--preserve-tabs")
        
        # Create inline Lua filter for line break preservation
        lua_filter_content = '''
function Para(elem)
  -- Convert soft breaks to hard breaks in paragraphs
  local new_content = {}
  for i, item in ipairs(elem.content) do
    table.insert(new_content, item)
    if item.t == "SoftBreak" then
      -- Replace SoftBreak with LineBreak
      new_content[#new_content] = pandoc.LineBreak()
    end
  end
  elem.content = new_content
  return elem
end

function LineBlock(elem)
  -- Preserve line blocks as they are
  return elem
end

function RawBlock(elem)
  -- Preserve raw LaTeX blocks
  if elem.format == "latex" then
    return elem
  end
end
'''
        
        # Create temporary Lua filter file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as f:
            f.write(lua_filter_content)
            lua_filter_path = f.name
        
        extra_args.append(f"--lua-filter={lua_filter_path}")

    try:
        # Perform conversion
        pypandoc.convert_file(docx_path, 'latex', outputfile=latex_path, extra_args=extra_args)
        
        # Clean up temporary Lua filter if created
        if preserve_linebreaks and 'lua_filter_path' in locals():
            try:
                os.unlink(lua_filter_path)
            except OSError:
                pass
        
        # Apply post-processing enhancements
        if overleaf_compatible or preserve_styles or preserve_linebreaks:
            _apply_post_processing(latex_path, overleaf_compatible, preserve_styles, preserve_linebreaks, extract_media_to_path)
        
        # Generate status message
        enhancements = []
        if overleaf_compatible:
            enhancements.append("Overleaf compatibility")
        if preserve_styles:
            enhancements.append("style preservation")
        if preserve_linebreaks:
            enhancements.append("line break preservation")
        
        if enhancements:
            enhancement_msg = f" with {', '.join(enhancements)}"
        else:
            enhancement_msg = ""
            
        return True, f"Conversion successful{enhancement_msg}!"
        
    except RuntimeError as e:
        # Clean up temporary Lua filter if created
        if preserve_linebreaks and 'lua_filter_path' in locals():
            try:
                os.unlink(lua_filter_path)
            except OSError:
                pass
        return False, f"RuntimeError: Could not execute Pandoc. Please ensure Pandoc is installed and in your system's PATH. Error: {e}"
    except Exception as e:
        # Clean up temporary Lua filter if created
        if preserve_linebreaks and 'lua_filter_path' in locals():
            try:
                os.unlink(lua_filter_path)
            except OSError:
                pass
        return False, f"Conversion failed: {e}"

def _apply_post_processing(latex_path: str, overleaf_compatible: bool, preserve_styles: bool, preserve_linebreaks: bool, extract_media_to_path: str = None):
    """
    Apply post-processing enhancements to the generated LaTeX file.
    """
    try:
        with open(latex_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Always inject essential packages for compilation compatibility
        content = _inject_essential_packages(content)
        
        # Apply overleaf compatibility fixes
        if overleaf_compatible:
            content = _fix_image_paths_for_overleaf(content, extract_media_to_path)
        
        # Apply style preservation enhancements
        if preserve_styles:
            content = _inject_latex_packages(content)
            content = _add_centering_commands(content)
        
        # Apply line break preservation fixes
        if preserve_linebreaks:
            content = _fix_line_breaks_and_spacing(content)
        
        # Fix common LaTeX compilation issues
        content = _fix_compilation_issues(content)
        
        # Write back the processed content
        with open(latex_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        # Post-processing failures shouldn't break the conversion
        print(f"Warning: Post-processing failed: {e}")

def _inject_essential_packages(content: str) -> str:
    """
    Inject essential packages that are always needed for compilation.
    """
    # Core packages that Pandoc might not include but are often needed
    essential_packages = [
        r'\usepackage[utf8]{inputenc}',  # UTF-8 input encoding
        r'\usepackage[T1]{fontenc}',     # Font encoding
        r'\usepackage{graphicx}',        # For images
        r'\usepackage{longtable}',       # For tables
        r'\usepackage{booktabs}',        # Better table formatting
        r'\usepackage{hyperref}',        # For links (if not already included)
    ]
    
    documentclass_pattern = r'\\documentclass(?:\[[^\]]*\])?\{[^}]+\}'
    documentclass_match = re.search(documentclass_pattern, content)
    
    if documentclass_match:
        insert_pos = documentclass_match.end()
        
        packages_to_insert = []
        for package in essential_packages:
            package_name = package.split('{')[1].split('}')[0].split(']')[0]  # Extract package name
            if f'usepackage' not in content or package_name not in content:
                packages_to_insert.append(package)
        
        if packages_to_insert:
            package_block = '\n% Essential packages for compilation\n' + '\n'.join(packages_to_insert) + '\n'
            content = content[:insert_pos] + package_block + content[insert_pos:]
    
    return content

def _fix_compilation_issues(content: str) -> str:
    """
    Fix common LaTeX compilation issues.
    """
    # Fix \tightlist command if not defined
    if r'\tightlist' in content and r'\providecommand{\tightlist}' not in content:
        tightlist_def = r'''
% Define \tightlist command for lists
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
'''
        # Insert after packages but before \begin{document}
        begin_doc_match = re.search(r'\\begin\{document\}', content)
        if begin_doc_match:
            insert_pos = begin_doc_match.start()
            content = content[:insert_pos] + tightlist_def + '\n' + content[insert_pos:]
    
    # Fix \euro command if used but not defined
    if r'\euro' in content and r'usepackage{eurosym}' not in content:
        content = re.sub(
            r'(\\usepackage\{[^}]+\}\s*\n)',
            r'\1\\usepackage{eurosym}\n',
            content,
            count=1
        )
    
    # Fix undefined references to figures/tables
    content = re.sub(r'\\ref\{fig:([^}]+)\}', r'Figure~\\ref{fig:\1}', content)
    content = re.sub(r'\\ref\{tab:([^}]+)\}', r'Table~\\ref{tab:\1}', content)
    
    # Ensure proper figure placement
    if r'\begin{figure}' in content:
        content = re.sub(
            r'\\begin\{figure\}(?!\[)',
            r'\\begin{figure}[htbp]',
            content
        )
    
    # Ensure proper table placement  
    if r'\begin{table}' in content:
        content = re.sub(
            r'\\begin\{table\}(?!\[)',
            r'\\begin{table}[htbp]',
            content
        )
    
    return content

def _fix_image_paths_for_overleaf(content: str, extract_media_to_path: str = None) -> str:
    """
    Convert absolute image paths to relative paths for Overleaf compatibility.
    """
    if extract_media_to_path:
        # Extract the media directory name
        media_dir = os.path.basename(extract_media_to_path.rstrip('/'))
        # Replace absolute paths with relative paths
        # Pattern: \includegraphics{/absolute/path/to/media/image.ext}
        # Replace with: \includegraphics{media/image.ext}
        pattern = r'\\includegraphics(\[[^\]]*\])?\{[^{}]*[/\\]' + re.escape(media_dir) + r'[/\\]([^{}]+)\}'
        replacement = r'\\includegraphics\1{' + media_dir + r'/\2}'
        content = re.sub(pattern, replacement, content)
    
    return content

def _inject_latex_packages(content: str) -> str:
    """
    Inject additional LaTeX packages needed for enhanced formatting.
    """
    # Essential packages for enhanced conversion
    essential_packages = [
        r'\usepackage{graphicx}',      # For images - ensure it's included
        r'\usepackage{longtable}',     # For tables
        r'\usepackage{booktabs}',      # Better table formatting  
        r'\usepackage{array}',         # Enhanced table formatting
        r'\usepackage{calc}',          # For calculations
        r'\usepackage{url}',           # For URLs
    ]
    
    # Style enhancement packages
    style_packages = [
        r'\usepackage{float}',         # Better float positioning
        r'\usepackage{adjustbox}',     # For centering and scaling
        r'\usepackage{caption}',       # Better caption formatting
        r'\usepackage{subcaption}',    # For subfigures
        r'\usepackage{tabularx}',      # Flexible table widths
        r'\usepackage{enumitem}',      # Better list formatting
        r'\usepackage{setspace}',      # Line spacing control
        r'\usepackage{ragged2e}',      # Better text alignment
        r'\usepackage{amsmath}',       # Mathematical formatting
        r'\usepackage{amssymb}',       # Mathematical symbols
    ]
    
    all_packages = essential_packages + style_packages
    
    # Find the position after \documentclass but before any existing \usepackage or \begin{document}
    documentclass_pattern = r'\\documentclass(?:\[[^\]]*\])?\{[^}]+\}'
    documentclass_match = re.search(documentclass_pattern, content)
    
    if documentclass_match:
        insert_pos = documentclass_match.end()
        
        # Find the next significant LaTeX command to insert before it
        # Look for existing \usepackage, \begin{document}, or other commands
        remaining_content = content[insert_pos:]
        next_command_match = re.search(r'\\(?:usepackage|begin\{document\}|title|author|date)', remaining_content)
        
        if next_command_match:
            insert_pos += next_command_match.start()
        
        # Check which packages are not already included
        packages_to_insert = []
        for package in all_packages:
            package_name = package.replace(r'\usepackage{', '').replace('}', '')
            if f'usepackage{{{package_name}}}' not in content:
                packages_to_insert.append(package)
        
        if packages_to_insert:
            # Add packages with proper spacing
            package_block = '\n% Enhanced conversion packages\n' + '\n'.join(packages_to_insert) + '\n\n'
            content = content[:insert_pos] + package_block + content[insert_pos:]
    
    return content

def _add_centering_commands(content: str) -> str:
    """
    Add centering commands to figures and tables.
    """
    # Add \centering to figure environments
    content = re.sub(
        r'(\\begin\{figure\}(?:\[[^\]]*\])?)\s*\n',
        r'\1\n\\centering\n',
        content
    )
    
    # Add \centering to table environments
    content = re.sub(
        r'(\\begin\{table\}(?:\[[^\]]*\])?)\s*\n',
        r'\1\n\\centering\n',
        content
    )
    
    return content

def _fix_line_breaks_and_spacing(content: str) -> str:
    """
    Fix line break and spacing issues for better formatting.
    """
    # Fix spacing around numbered lists (enumerate)
    content = re.sub(r'\n\\begin\{enumerate\}\n\n', r'\n\\begin{enumerate}\n', content)
    content = re.sub(r'\n\n\\end\{enumerate\}\n', r'\n\\end{enumerate}\n\n', content)
    
    # Fix spacing around bullet lists (itemize)
    content = re.sub(r'\n\\begin\{itemize\}\n\n', r'\n\\begin{itemize}\n', content)
    content = re.sub(r'\n\n\\end\{itemize\}\n', r'\n\\end{itemize}\n\n', content)
    
    # Fix excessive spacing between list items
    content = re.sub(r'\\item\s*\n\n+', r'\\item ', content)
    
    # Fix spacing around section headings
    content = re.sub(r'\n\n(\\(?:sub)*section\{[^}]+\})\n\n', r'\n\n\1\n', content)
    
    # Fix paragraph spacing issues
    content = re.sub(r'\n\n\n+', r'\n\n', content)
    
    return content

if __name__ == '__main__':
    from docx import Document
    from docx.shared import Inches
    from PIL import Image
    import shutil

    # --- Helper Functions for DOCX and Template Creation ---
    def create_dummy_image(filename, size=(60, 60), color="red", img_format="PNG"):
        img = Image.new('RGB', size, color=color)
        img.save(filename, img_format)
        print(f"Created dummy image: {filename}")

    def create_test_docx_with_styles(filename):
        doc = Document()
        doc.add_heading("Document with Enhanced Features", level=1)
        
        # Add paragraph with text
        p1 = doc.add_paragraph("This document tests enhanced features including:")
        
        # Add numbered list
        doc.add_paragraph("First numbered item", style='List Number')
        doc.add_paragraph("Second numbered item", style='List Number')
        doc.add_paragraph("Third numbered item", style='List Number')
        
        # Add some text
        doc.add_paragraph("Here is some regular text between lists.")
        
        # Add bullet list
        doc.add_paragraph("First bullet point", style='List Bullet')
        doc.add_paragraph("Second bullet point", style='List Bullet')
        
        doc.add_heading("Image Section", level=2)
        doc.add_paragraph("Below is a test image:")
        
        doc.save(filename)
        print(f"Created test DOCX with styles: {filename}")

    def create_complex_docx(filename, img1_path, img2_path):
        doc = Document()
        doc.add_heading("Complex Document Title", level=1)
        doc.add_paragraph("Introduction to the complex document.")
        doc.add_heading("Image Section", level=2)
        doc.add_picture(img1_path, width=Inches(1.0))
        doc.add_paragraph("Some text after the first image.")
        doc.add_picture(img2_path, width=Inches(1.0))
        doc.add_heading("Conclusion Section", level=2)
        doc.add_paragraph("Final remarks.")
        doc.save(filename)
        print(f"Created complex DOCX: {filename}")

    # --- Test Files ---
    docx_styles = "test_enhanced_styles.docx"
    docx_complex = "test_complex_enhanced.docx"
    img1 = "dummy_img1.png"
    img2 = "dummy_img2.jpg"

    output_enhanced_test = "output_enhanced_test.tex"
    output_overleaf_test = "output_overleaf_test.tex"
    media_dir = "./media_enhanced"

    all_test_files = [docx_styles, docx_complex, img1, img2, output_enhanced_test, output_overleaf_test]
    all_test_dirs = [media_dir]

    # --- Create Test Files ---
    print("--- Setting up enhanced test files ---")
    create_dummy_image(img1, color="blue", img_format="PNG")
    create_dummy_image(img2, color="green", img_format="JPEG")
    create_test_docx_with_styles(docx_styles)
    create_complex_docx(docx_complex, img1, img2)
    print("--- Enhanced test file setup complete ---")

    # --- Test Enhanced Features ---
    print("\n--- Testing Enhanced Features ---")

    # Test 1: Style preservation and line breaks
    print("\n--- Test 1: Enhanced Style Preservation ---")
    success, msg = convert_docx_to_latex(
        docx_styles, 
        output_enhanced_test,
        generate_toc=True,
        preserve_styles=True,
        preserve_linebreaks=True
    )
    print(f"Enhanced Test: {success}, Msg: {msg}")
    
    if success and os.path.exists(output_enhanced_test):
        with open(output_enhanced_test, 'r') as f:
            content = f.read()
            checks = {
                'packages': any(pkg in content for pkg in ['\\usepackage{float}', '\\usepackage{enumitem}']),
                'toc': '\\tableofcontents' in content,
                'sections': '\\section' in content,
                'lists': '\\begin{enumerate}' in content or '\\begin{itemize}' in content
            }
            print(f"Enhanced verification: {checks}")

    # Test 2: Overleaf compatibility with images
    print("\n--- Test 2: Overleaf Compatibility ---")
    success, msg = convert_docx_to_latex(
        docx_complex,
        output_overleaf_test,
        extract_media_to_path=media_dir,
        overleaf_compatible=True,
        preserve_styles=True,
        preserve_linebreaks=True
    )
    print(f"Overleaf Test: {success}, Msg: {msg}")
    
    if success and os.path.exists(output_overleaf_test):
        with open(output_overleaf_test, 'r') as f:
            content = f.read()
            media_check = 'media/' in content and '\\includegraphics' in content
            print(f"Overleaf compatibility check - relative paths: {media_check}")
            
        media_files_exist = os.path.exists(os.path.join(media_dir, 'media'))
        print(f"Media files extracted: {media_files_exist}")

    # --- Cleanup ---
    print("\n--- Cleaning up enhanced test files ---")
    for f_path in all_test_files:
        if os.path.exists(f_path):
            try:
                os.remove(f_path)
                print(f"Removed: {f_path}")
            except Exception as e:
                print(f"Error removing {f_path}: {e}")

    for d_path in all_test_dirs:
        if os.path.isdir(d_path):
            try:
                shutil.rmtree(d_path)
                print(f"Removed directory: {d_path}")
            except Exception as e:
                print(f"Error removing {d_path}: {e}")

    print("--- Enhanced testing completed ---") 
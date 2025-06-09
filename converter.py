import pypandoc
import os

def convert_docx_to_latex(
    docx_path: str,
    latex_path: str,
    generate_toc: bool = False,
    extract_media_to_path: str = None,
    latex_template_path: str = None
) -> tuple[bool, str]:
    """
    Converts a DOCX file to a LaTeX file using pypandoc.

    Args:
        docx_path: Path to the input .docx file.
        latex_path: Path to save the output .tex file.
        generate_toc: If True, attempts to generate a Table of Contents.
        extract_media_to_path: If specified, path to extract media to (e.g., "./media").
        latex_template_path: If specified, path to a custom Pandoc LaTeX template file.

    Returns:
        A tuple (success: bool, message: str).
    """
    extra_args = []
    if generate_toc:
        extra_args.append("--toc")
    if extract_media_to_path:
        extra_args.append(f"--extract-media={extract_media_to_path}")
    if latex_template_path and os.path.isfile(latex_template_path):
        extra_args.append(f"--template={latex_template_path}")
    elif latex_template_path:
        # It's good practice to warn or handle if a template path is given but not found,
        # but for now, Pandoc will error out, and we'll return that error.
        # Alternatively, could return a (False, "Custom template not found...") message here.
        pass


    try:
        pypandoc.convert_file(docx_path, 'latex', outputfile=latex_path, extra_args=extra_args)
        return True, "Conversion successful!"
    except RuntimeError as e:
        return False, f"RuntimeError: Could not execute Pandoc. Please ensure Pandoc is installed and in your system's PATH. Error: {e}"
    except Exception as e:
        return False, f"Conversion failed: {e}"

if __name__ == '__main__':
    from docx import Document
    from docx.shared import Inches
    from PIL import Image
    import shutil
    import re # For searching content in output files

    # --- Helper Functions for DOCX and Template Creation ---
    def create_dummy_image(filename, size=(60, 60), color="red", img_format="PNG"):
        img = Image.new('RGB', size, color=color)
        img.save(filename, img_format)
        print(f"Created dummy image: {filename}")

    def create_headings_docx(filename):
        doc = Document()
        doc.add_heading("Main Heading Level 1", level=1)
        doc.add_paragraph("Some text under H1.")
        doc.add_heading("Subheading Level 2", level=2)
        doc.add_paragraph("Some text under H2.")
        doc.add_heading("Sub-subheading Level 3", level=3)
        doc.add_paragraph("Some text under H3.")
        doc.save(filename)
        print(f"Created DOCX with headings: {filename}")

    def create_images_docx(filename, img1_path, img2_path):
        doc = Document()
        doc.add_paragraph("Document with two images.")
        doc.add_picture(img1_path, width=Inches(1.0))
        doc.add_paragraph("Second image below.")
        doc.add_picture(img2_path, width=Inches(1.0))
        doc.save(filename)
        print(f"Created DOCX with images: {filename}")

    def create_simple_docx(filename):
        doc = Document()
        doc.add_paragraph("This is a simple test document with a single paragraph.")
        doc.save(filename)
        print(f"Created simple DOCX: {filename}")

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

    def create_minimal_latex_template(filename):
        content = """
\\documentclass{article}
\\usepackage{graphicx} % For images, if not automatically handled by pandoc with template
\\usepackage{booktabs} % For tables, if not automatically handled
\\usepackage{longtable} % For tables
\\usepackage{array} % For tables
\\usepackage{multirow} % For tables
% It's often better to let Pandoc handle package loading if possible,
% but for a truly minimal test, explicitly adding them can be useful.
$if(title)$
  \\title{$title$}
  \\author{$for(author)$$author$$sep$, $endfor$}
  \\date{$date$}
$endif$
\\begin{document}
$if(title)$
  \\maketitle
$endif$
$if(toc)$
\\tableofcontents
\\newpage
$endif$
$body$
\\end{document}
"""
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Created minimal LaTeX template: {filename}")

    # --- File Names for Test ---
    docx_headings = "test_headings.docx"
    docx_images = "test_images.docx"
    docx_simple = "test_simple.docx"
    docx_complex = "test_complex.docx"

    img1 = "dummy_img1.png"
    img2 = "dummy_img2.jpg"

    template_file = "minimal_test_template.tex"

    output_toc_test = "output_toc_test.tex"
    output_imgext_test = "output_imgext_test.tex"
    media_consolidated_imgext = "./media_consolidated_imgext" # Note: Pandoc creates 'media' inside this

    output_template_test = "output_template_test.tex"

    output_complex_test = "output_complex_test.tex"
    media_consolidated_complex = "./media_consolidated_complex" # Note: Pandoc creates 'media' inside this

    all_generated_files = [
        docx_headings, docx_images, docx_simple, docx_complex,
        img1, img2, template_file,
        output_toc_test, output_imgext_test, output_template_test, output_complex_test
    ]
    all_generated_dirs = [media_consolidated_imgext, media_consolidated_complex]

    # --- Create all input files ---
    print("--- Setting up test files ---")
    create_dummy_image(img1, color="blue", img_format="PNG")
    create_dummy_image(img2, color="green", img_format="JPEG")
    create_headings_docx(docx_headings)
    create_images_docx(docx_images, img1, img2)
    create_simple_docx(docx_simple)
    create_complex_docx(docx_complex, img1, img2)
    create_minimal_latex_template(template_file)
    print("--- Test file setup complete ---")

    # --- Execute Test Cases ---
    print("\n--- Running Test Cases ---")

    # Test Case 1: ToC Generation
    print("\n--- Test Case 1: ToC Generation ---")
    success, msg = convert_docx_to_latex(docx_headings, output_toc_test, generate_toc=True)
    print(f"TC1 Conversion: {success}, Msg: {msg}")
    if success and os.path.exists(output_toc_test) and os.path.getsize(output_toc_test) > 0:
        print(f"'{output_toc_test}' created and non-empty.")
        with open(output_toc_test, 'r') as f:
            content = f.read()
            if r"\section" in content and r"\subsection" in content:
                print("TC1 Verification: \\section and \\subsection commands found.")
            else:
                print("TC1 Verification FAILED: Expected sectioning commands not found.")
    else:
        print(f"TC1 FAILED: Output file not created or empty.")

    # Test Case 2: Image Extraction
    print("\n--- Test Case 2: Image Extraction ---")
    success, msg = convert_docx_to_latex(docx_images, output_imgext_test, extract_media_to_path=media_consolidated_imgext)
    print(f"TC2 Conversion: {success}, Msg: {msg}")
    expected_media_dir_tc2 = os.path.join(media_consolidated_imgext, "media")
    if success and os.path.exists(output_imgext_test) and os.path.getsize(output_imgext_test) > 0:
        print(f"'{output_imgext_test}' created and non-empty.")
        if os.path.isdir(expected_media_dir_tc2) and len(os.listdir(expected_media_dir_tc2)) >= 2:
            print(f"TC2 Verification: Media directory '{expected_media_dir_tc2}' created with files: {os.listdir(expected_media_dir_tc2)}")
        else:
            print(f"TC2 Verification FAILED: Media directory '{expected_media_dir_tc2}' not found or doesn't contain expected files. Found: {os.listdir(media_consolidated_imgext) if os.path.exists(media_consolidated_imgext) else 'None'}")
        with open(output_imgext_test, 'r') as f:
            content = f.read()
            if r"\includegraphics" in content and media_consolidated_imgext in content:
                 print("TC2 Verification: \\includegraphics commands referencing extracted media path found.")
            else:
                print("TC2 Verification FAILED: Expected \\includegraphics commands not found or path incorrect.")
    else:
        print(f"TC2 FAILED: Output file not created or empty.")

    # Test Case 3: Custom Template
    print("\n--- Test Case 3: Custom Template ---")
    success, msg = convert_docx_to_latex(docx_simple, output_template_test, latex_template_path=template_file)
    print(f"TC3 Conversion: {success}, Msg: {msg}")
    if success and os.path.exists(output_template_test) and os.path.getsize(output_template_test) > 0:
        print(f"'{output_template_test}' created and non-empty.")
        with open(output_template_test, 'r') as f:
            content = f.read()
            # Check if it's using the minimal template structure, not the full pandoc default
            if r"\documentclass{article}" in content and "$if(toc)$" not in content and "This is a simple test document" in content:
                if r"\tableofcontents" not in content: # Since generate_toc=False
                    print("TC3 Verification: Output matches minimal template structure and no ToC present.")
                else:
                    print("TC3 Verification FAILED: ToC present despite generate_toc=False with custom template.")
            else:
                print("TC3 Verification FAILED: Output does not seem to use the minimal template.")
    else:
        print(f"TC3 FAILED: Output file not created or empty.")

    # Test Case 4: All Options Combined
    print("\n--- Test Case 4: All Options Combined ---")
    success, msg = convert_docx_to_latex(docx_complex, output_complex_test,
                                         generate_toc=True,
                                         extract_media_to_path=media_consolidated_complex,
                                         latex_template_path=template_file)
    print(f"TC4 Conversion: {success}, Msg: {msg}")
    expected_media_dir_tc4 = os.path.join(media_consolidated_complex, "media")
    if success and os.path.exists(output_complex_test) and os.path.getsize(output_complex_test) > 0:
        print(f"'{output_complex_test}' created and non-empty.")
        # Media check
        if os.path.isdir(expected_media_dir_tc4) and len(os.listdir(expected_media_dir_tc4)) >= 2:
            print(f"TC4 Verification: Media directory '{expected_media_dir_tc4}' created with files: {os.listdir(expected_media_dir_tc4)}")
        else:
            print(f"TC4 Verification FAILED: Media directory '{expected_media_dir_tc4}' not found or doesn't contain expected files.")
        # Content check (ToC, includegraphics, body)
        with open(output_complex_test, 'r') as f:
            content = f.read()
            toc_present = r"\tableofcontents" in content
            includegraphics_present = r"\includegraphics" in content and media_consolidated_complex in content
            body_text_present = "Introduction to the complex document" in content
            if toc_present and includegraphics_present and body_text_present:
                print("TC4 Verification: ToC, includegraphics (with correct path), and body content found.")
            else:
                print(f"TC4 Verification FAILED: ToC={toc_present}, includegraphics correct path={includegraphics_present}, body_text={body_text_present}")
    else:
        print(f"TC4 FAILED: Output file not created or empty.")

    # --- Cleanup ---
    print("\n--- Cleaning up all generated test files and directories ---")
    for f_path in all_generated_files:
        if os.path.exists(f_path):
            try:
                os.remove(f_path)
                print(f"Removed file: {f_path}")
            except Exception as e:
                print(f"Error removing file {f_path}: {e}")

    for d_path in all_generated_dirs:
        if os.path.isdir(d_path):
            try:
                shutil.rmtree(d_path)
                print(f"Removed directory: {d_path}")
            except Exception as e:
                print(f"Error removing directory {d_path}: {e}")

    print("--- Consolidated Testing Completed ---")

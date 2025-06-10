import pypandoc
import os

def convert_docx_to_latex(
    docx_path: str,
    latex_path: str,
    generate_toc: bool = False,
    extract_media_to_path: str = None,
    latex_template_path: str = None,
    apply_known_styles_filter: bool = False,
    from_format_spec: str = None
) -> tuple[bool, str]:
    """
    Converts a DOCX file to a LaTeX file using pypandoc.
    Args:
        docx_path: Path to the input .docx file.
        latex_path: Path to save the output .tex file.
        generate_toc: If True, attempts to generate a Table of Contents.
        extract_media_to_path: If specified, path to extract media to. Pandoc creates "media" subdir here.
        latex_template_path: If specified, path to a custom Pandoc LaTeX template file.
        apply_known_styles_filter: If True, applies 'handle_known_styles.lua'.
        from_format_spec: If specified, uses this as the 'format' arg for pypandoc.
    Returns:
        A tuple (success: bool, message: str).
    """
    extra_args = []
    input_format = from_format_spec if from_format_spec else 'docx'

    if generate_toc:
        extra_args.append("--toc")
    if extract_media_to_path:
        extra_args.append(f"--extract-media={extract_media_to_path}")
    if latex_template_path and os.path.isfile(latex_template_path):
        extra_args.append(f"--template={latex_template_path}")
    elif latex_template_path:
        print(f"Warning: Custom template '{latex_template_path}' not found. Using Pandoc default.")

    if apply_known_styles_filter:
        lua_filter_script_path = "./handle_known_styles.lua"
        if os.path.isfile(lua_filter_script_path):
            extra_args.append(f"--lua-filter={lua_filter_script_path}")
        else:
            print(f"Warning: Lua filter '{lua_filter_script_path}' not found. Proceeding without it.")

    try:
        pypandoc.convert_file(
            docx_path,
            'latex',
            format=input_format,
            outputfile=latex_path,
            extra_args=extra_args
        )
        return True, "Conversion successful!"
    except RuntimeError as e:
        return False, f"RuntimeError: Could not execute Pandoc. Please ensure Pandoc is installed and in your system's PATH. Error: {e}"
    except Exception as e:
        return False, f"Conversion failed: {e}"

if __name__ == '__main__':
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.enum.style import WD_STYLE_TYPE
    from PIL import Image
    import shutil
    import re

    master_generated_files = []
    master_generated_dirs = []

    # --- Helper Functions ---
    def create_dummy_image(filename, size=(60, 60), color="red", img_format="PNG"):
        img = Image.new('RGB', size, color=color)
        img.save(filename, img_format)
        print(f"Created dummy image: {filename}")
        master_generated_files.append(filename)

    def create_headings_docx(filename):
        doc = Document()
        doc.add_heading("Main Heading Level 1", level=1)
        doc.add_paragraph("Some text under H1.")
        doc.add_heading("Subheading Level 2", level=2)
        doc.add_paragraph("Some text under H2.")
        doc.add_heading("Sub-subheading Level 3", level=3)
        doc.add_paragraph("Some text under H3.")
        doc.save(filename)
        print(f"Created DOCX: {filename}")
        master_generated_files.append(filename)

    def create_images_docx(filename, img1_path, img2_path):
        doc = Document()
        doc.add_paragraph("Document with two images.")
        doc.add_picture(img1_path, width=Inches(1.0))
        doc.add_paragraph("Second image below.")
        doc.add_picture(img2_path, width=Inches(1.0))
        doc.save(filename)
        print(f"Created DOCX: {filename}")
        master_generated_files.append(filename)

    def create_simple_docx(filename):
        doc = Document()
        doc.add_paragraph("This is a simple test document with a single paragraph.")
        doc.save(filename)
        print(f"Created DOCX: {filename}")
        master_generated_files.append(filename)

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
        print(f"Created DOCX: {filename}")
        master_generated_files.append(filename)

    def create_line_breaks_docx(filename):
        doc = Document()
        doc.add_heading("Line Break Test Document", level=1)
        doc.add_paragraph("First item, first line.", style='ListNumber')
        p2 = doc.add_paragraph("Second item, first line.", style='ListNumber')
        p2.runs[0].add_break(WD_BREAK.LINE)
        p2.add_run("Second item, second line on soft break.")
        doc.add_paragraph("This is a paragraph after the list.")
        p3 = doc.add_paragraph("Third item, first line.", style='ListNumber')
        p3.runs[0].add_break(WD_BREAK.LINE)
        p3.add_run("Third item, second line on soft break.")
        p3.runs[-1].add_break(WD_BREAK.LINE)
        p3.add_run("Third item, third line on soft break.")
        doc.save(filename)
        print(f"Created DOCX: {filename}")
        master_generated_files.append(filename)

    def create_minimal_latex_template(filename):
        content = """
\\documentclass{article}
\\usepackage{graphicx}
\\usepackage{booktabs}
\\usepackage{longtable}
\\usepackage{array}
\\usepackage{multirow}
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
        print(f"Created LaTeX template: {filename}")
        master_generated_files.append(filename)

    def create_lua_filter(filename):
        content = """
-- handle_known_styles.lua
function Para (el)
  if el.attributes and el.attributes['custom-style'] and el.attributes['custom-style'] == 'DocxToLatexCentered' then
    local content_latex = pandoc.write(pandoc.Pandoc(pandoc.Plain(el.content)), 'latex')
    content_latex = content_latex:gsub("^\\pard?%s*", ""):gsub("\\par?%s*$", "")
    content_latex = content_latex:gsub("^\n*", ""):gsub("\n*$", "")
    return pandoc.RawBlock('latex', '\\begin{center}\n' .. content_latex .. '\n\\end{center}')
  end
  return el
end
"""
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Created Lua filter: {filename}")
        master_generated_files.append(filename)

    # --- Test File Names ---
    docx_h = "final_test_headings.docx"
    docx_i = "final_test_images.docx"
    img_1 = "final_img1.png"
    img_2 = "final_img2.jpg"
    docx_s = "final_test_simple.docx"
    docx_lb = "final_test_line_breaks.docx"
    docx_c = "final_test_complex.docx"
    template_f = "final_minimal_template.tex"
    lua_f = "handle_known_styles.lua" # Ensure this is consistently named

    # --- Create All Input Files ---
    print("--- Setting up all test input files ---")
    create_dummy_image(img_1, color="magenta")
    create_dummy_image(img_2, color="cyan", img_format="JPEG")
    create_headings_docx(docx_h)
    create_images_docx(docx_i, img_1, img_2)
    create_simple_docx(docx_s)
    create_line_breaks_docx(docx_lb)
    create_complex_docx(docx_c, img_1, img_2)
    create_minimal_latex_template(template_f)
    create_lua_filter(lua_f) # Create the Lua filter for tests that need it
    print("--- All test input files created ---")

    # --- Test Execution ---
    print("\n--- Running Final Consolidated Test Cases ---")

    # Test Case 1: ToC Generation (Regression Check)
    print("\n--- TC1: ToC Generation ---")
    tc1_out = "final_output_toc.tex"
    master_generated_files.append(tc1_out)
    succ, msg = convert_docx_to_latex(docx_h, tc1_out, generate_toc=True)
    print(f"TC1 Result: {succ}, Msg: {msg}")
    if succ and os.path.exists(tc1_out):
        with open(tc1_out, 'r', encoding='utf-8') as f: content = f.read()
        if r"\section" in content and r"\subsection" in content: print("TC1 Verification: PASSED")
        else: print("TC1 Verification: FAILED - Sectioning commands missing.")
    else: print(f"TC1 Verification: FAILED - Output file not created or conversion failed.")

    # Test Case 2: Image Extraction (New Pathing)
    print("\n--- TC2: Image Extraction (New Pathing) ---")
    tc2_out = "final_output_imgext.tex"
    master_generated_files.append(tc2_out)
    # Media dir will be "./media" relative to where script is run.
    master_generated_dirs.append("./media") # Add only once, even if multiple tests use it.
    succ, msg = convert_docx_to_latex(docx_i, tc2_out, extract_media_to_path=".")
    print(f"TC2 Result: {succ}, Msg: {msg}")
    if succ and os.path.exists(tc2_out):
        with open(tc2_out, 'r', encoding='utf-8') as f: content = f.read()
        img1_ok = bool(re.search(r"\\includegraphics\[.*?\]\{(\./)?media/image1\.png\}", content))
        img2_ok = bool(re.search(r"\\includegraphics\[.*?\]\{(\./)?media/image2\.jpg\}", content))
        media_dir_ok = os.path.isdir("./media") and len(os.listdir("./media")) >= 2
        if img1_ok and img2_ok and media_dir_ok: print("TC2 Verification: PASSED")
        else: print(f"TC2 Verification: FAILED - Img1:{img1_ok}, Img2:{img2_ok}, MediaDir:{media_dir_ok} (Files: {os.listdir('./media') if media_dir_ok else 'None'})")
    else: print(f"TC2 Verification: FAILED - Output file not created or conversion failed.")

    # Test Case 3: Custom Template (Regression Check)
    print("\n--- TC3: Custom Template ---")
    tc3_out = "final_output_template.tex"
    master_generated_files.append(tc3_out)
    succ, msg = convert_docx_to_latex(docx_s, tc3_out, latex_template_path=template_f)
    print(f"TC3 Result: {succ}, Msg: {msg}")
    if succ and os.path.exists(tc3_out):
        with open(tc3_out, 'r', encoding='utf-8') as f: content = f.read()
        if r"\documentclass{article}" in content and "This is a simple test document" in content and "$if(toc)$" not in content and r"\tableofcontents" not in content:
             print("TC3 Verification: PASSED")
        else: print("TC3 Verification: FAILED - Output does not match minimal template structure.")
    else: print(f"TC3 Verification: FAILED - Output file not created or conversion failed.")

    # Test Case 4: Centering Filter Mechanism (Option Passing Check)
    print("\n--- TC4: Centering Filter Mechanism ---")
    tc4_out = "final_output_filter_test.tex"
    master_generated_files.append(tc4_out)
    # Using test_complex.docx which has no "DocxToLatexCentered" style, so no centering expected.
    succ, msg = convert_docx_to_latex(docx_c, tc4_out, apply_known_styles_filter=True)
    print(f"TC4 Result: {succ}, Msg: {msg}")
    if succ and os.path.exists(tc4_out):
        with open(tc4_out, 'r', encoding='utf-8') as f: content = f.read()
        if r"\begin{center}" not in content: print("TC4 Verification: PASSED (Filter called, no centering applied as expected).")
        else: print("TC4 Verification: FAILED - Unexpected centering applied.")
    else: print(f"TC4 Verification: FAILED - Output file not created or conversion failed.")

    # Test Case 5: Line Break Default Handling (Verification)
    print("\n--- TC5: Line Break Default Handling ---")
    tc5_out = "final_output_line_breaks.tex"
    master_generated_files.append(tc5_out)
    succ, msg = convert_docx_to_latex(docx_lb, tc5_out)
    print(f"TC5 Result: {succ}, Msg: {msg}")
    if succ and os.path.exists(tc5_out):
        with open(tc5_out, 'r', encoding='utf-8') as f: content = f.read()
        # Check for "line.\\" which indicates soft break conversion
        if "Second item, first line.\\\\" in content and "Third item, second line on soft break.\\\\" in content:
            print("TC5 Verification: PASSED (Soft line breaks rendered as \\\\).")
        else: print(f"TC5 Verification: FAILED - Expected soft line break handling not found. Content: {content[:500]}")
    else: print(f"TC5 Verification: FAILED - Output file not created or conversion failed.")

    # Test Case 6: All Options Combined (New Pathing and Filter Option)
    print("\n--- TC6: All Options Combined ---")
    tc6_out = "final_output_complex.tex"
    master_generated_files.append(tc6_out)
    # master_generated_dirs.append("./media") # Already added in TC2, set will handle duplicates
    succ, msg = convert_docx_to_latex(docx_c, tc6_out,
                                      generate_toc=True,
                                      extract_media_to_path=".",
                                      latex_template_path=template_f,
                                      apply_known_styles_filter=True)
    print(f"TC6 Result: {succ}, Msg: {msg}")
    if succ and os.path.exists(tc6_out):
        with open(tc6_out, 'r', encoding='utf-8') as f: content = f.read()
        toc_ok = r"\tableofcontents" in content
        img1_ok_tc6 = bool(re.search(r"\\includegraphics\[.*?\]\{(\./)?media/image1\.png\}", content))
        img2_ok_tc6 = bool(re.search(r"\\includegraphics\[.*?\]\{(\./)?media/image2\.jpg\}", content))
        media_dir_ok_tc6 = os.path.isdir("./media") and len(os.listdir("./media")) >= 2
        template_applied_tc6 = r"\documentclass{article}" in content and "$if(toc)$" not in content
        filter_no_center_tc6 = r"\begin{center}" not in content # Since test_complex.docx has no "DocxToLatexCentered" style

        if toc_ok and img1_ok_tc6 and img2_ok_tc6 and media_dir_ok_tc6 and template_applied_tc6 and filter_no_center_tc6:
            print("TC6 Verification: PASSED")
        else:
            print(f"TC6 Verification: FAILED - ToC:{toc_ok}, Img1:{img1_ok_tc6}, Img2:{img2_ok_tc6}, MediaDir:{media_dir_ok_tc6} (Files: {os.listdir('./media') if media_dir_ok_tc6 else 'None'}), Template:{template_applied_tc6}, NoCenter:{filter_no_center_tc6}")
    else: print(f"TC6 Verification: FAILED - Output file not created or conversion failed.")

    # --- Final Combined Cleanup ---
    print("\n--- Final Cleanup of all test files ---")
    # Ensure potential AST files are added if they exist (though not generated by this script run directly)
    if os.path.exists("ast_line_breaks.json") and "ast_line_breaks.json" not in master_generated_files:
        master_generated_files.append("ast_line_breaks.json")
    if os.path.exists("ast_named_style.json") and "ast_named_style.json" not in master_generated_files:
        master_generated_files.append("ast_named_style.json")

    for f_path in list(set(master_generated_files)):
        if os.path.exists(f_path):
            try:
                os.remove(f_path)
                print(f"Final cleanup: Removed file: {f_path}")
            except Exception as e:
                print(f"Final cleanup error removing file {f_path}: {e}")

    for d_path in list(set(master_generated_dirs)):
        if os.path.isdir(d_path) and os.path.basename(os.path.abspath(d_path)) == "media": # Extra safety for "media"
            try:
                shutil.rmtree(d_path)
                print(f"Final cleanup: Removed directory: {d_path}")
            except Exception as e:
                print(f"Final cleanup error removing directory {d_path}: {e}")
        elif os.path.isdir(d_path): # For other potential dirs if added
             try:
                shutil.rmtree(d_path)
                print(f"Final cleanup: Removed directory: {d_path}")
             except Exception as e:
                print(f"Final cleanup error removing directory {d_path}: {e}")

    print("--- Script End ---")

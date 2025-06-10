import tkinter as tk
from tkinter import filedialog, messagebox
from converter import convert_docx_to_latex # Import the conversion function
import os # For path manipulation

# Global variables to store file paths
selected_docx_path = ""
output_tex_path = ""
selected_template_path = None # For custom LaTeX template

def select_docx_file():
    """Opens a file dialog to select a DOCX file."""
    global selected_docx_path
    filepath = filedialog.askopenfilename(
        title="Select DOCX File",
        filetypes=(("Word documents", "*.docx"), ("All files", "*.*"))
    )
    if filepath:
        selected_docx_path = filepath
        selected_docx_label.config(text=f"DOCX: {os.path.basename(selected_docx_path)}")
        status_label.config(text="", fg="black")
    else:
        selected_docx_label.config(text=f"DOCX: {os.path.basename(selected_docx_path) if selected_docx_path else 'No file selected.'}")

def select_output_tex_file():
    """Opens a file dialog to set the output .tex file path."""
    global output_tex_path
    filepath = filedialog.asksaveasfilename(
        title="Set Output LaTeX File",
        defaultextension=".tex",
        filetypes=(("LaTeX files", "*.tex"), ("All files", "*.*"))
    )
    if filepath:
        output_tex_path = filepath
        output_tex_label.config(text=f"Output: {os.path.basename(output_tex_path)}")
        status_label.config(text="", fg="black")
    else:
        output_tex_label.config(text=f"Output: {os.path.basename(output_tex_path) if output_tex_path else 'No file set.'}")

def select_template_file():
    """Opens a file dialog to select a custom LaTeX template file."""
    global selected_template_path
    filepath = filedialog.askopenfilename(
        title="Select Custom LaTeX Template (Optional)",
        filetypes=(("LaTeX Template Files", "*.tex"), ("All files", "*.*"))
    )
    if filepath:
        selected_template_path = filepath
        selected_template_label.config(text=f"Template: {os.path.basename(selected_template_path)}")
    else:
        selected_template_label.config(text=f"Template: {os.path.basename(selected_template_path) if selected_template_path else 'None (using Pandoc default)'}")
    status_label.config(text="", fg="black")

def clear_template_file():
    """Clears the selected custom LaTeX template."""
    global selected_template_path
    selected_template_path = None
    selected_template_label.config(text="Template: None (using Pandoc default)")
    status_label.config(text="", fg="black")

def show_help():
    """Show help dialog explaining the enhancement options."""
    help_text = """Enhancement Options Help:

🔧 Overleaf Compatible:
• Makes images work properly in Overleaf
• Converts absolute paths to relative paths
• Essential for cloud LaTeX editors

🎨 Preserve Styles:
• Maintains document formatting and styles
• Adds centering for figures and tables
• Includes additional LaTeX packages for better formatting
• Preserves text alignment and spacing

📝 Preserve Line Breaks:
• Fixes numbered list display issues
• Maintains proper paragraph spacing
• Prevents pagination problems
• Essential for documents with lists and structured content

💡 Tip: All options are enabled by default for best results!"""
    
    messagebox.showinfo("Enhancement Options Help", help_text)

def perform_conversion():
    """Performs the DOCX to LaTeX conversion with enhanced features."""
    global selected_docx_path, output_tex_path, selected_template_path

    if not selected_docx_path or not output_tex_path:
        status_label.config(text="Error: Please select both input DOCX and output .tex files.", fg="red")
        return

    if not os.path.exists(selected_docx_path):
        status_label.config(text="Error: Selected DOCX file does not exist.", fg="red")
        return

    # Determine media extraction path
    output_dir = os.path.dirname(output_tex_path)
    base_name_no_ext = os.path.splitext(os.path.basename(output_tex_path))[0]
    media_extract_path = os.path.join(output_dir, f"{base_name_no_ext}_media")

    status_label.config(text="Converting...", fg="blue")
    root.update_idletasks()

    # Get enhancement options
    generate_toc_option = toc_var.get()
    overleaf_compatible_option = overleaf_var.get()
    preserve_styles_option = styles_var.get()
    preserve_linebreaks_option = linebreaks_var.get()

    success, message = convert_docx_to_latex(
        selected_docx_path,
        output_tex_path,
        generate_toc=generate_toc_option,
        extract_media_to_path=media_extract_path,
        latex_template_path=selected_template_path,
        overleaf_compatible=overleaf_compatible_option,
        preserve_styles=preserve_styles_option,
        preserve_linebreaks=preserve_linebreaks_option
    )
    
    if success:
        status_label.config(text=message, fg="green")
    else:
        status_label.config(text=f"Error: {message}", fg="red")

# Create the main application window
root = tk.Tk()
root.title("Enhanced DOCX to LaTeX Converter")
root.geometry("600x700")
root.resizable(True, True)

# Create main frame with padding
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_label = tk.Label(main_frame, text="Enhanced DOCX to LaTeX Converter", 
                      font=("Arial", 16, "bold"), fg="navy")
title_label.pack(pady=(0, 20))

# --- File Selection Section ---
file_frame = tk.LabelFrame(main_frame, text="File Selection", font=("Arial", 12, "bold"), padx=10, pady=10)
file_frame.pack(fill=tk.X, pady=(0, 15))

# DOCX File Selection
select_docx_button = tk.Button(file_frame, text="Select DOCX File", command=select_docx_file, 
                              bg="lightblue", font=("Arial", 10))
select_docx_button.pack(pady=(5, 0))

selected_docx_label = tk.Label(file_frame, text="DOCX: No file selected.", 
                              wraplength=500, justify=tk.LEFT)
selected_docx_label.pack(pady=(5, 10))

# Output .tex File Selection
select_output_tex_button = tk.Button(file_frame, text="Set Output .tex File", command=select_output_tex_file,
                                    bg="lightgreen", font=("Arial", 10))
select_output_tex_button.pack(pady=(5, 0))

output_tex_label = tk.Label(file_frame, text="Output: No file set.", 
                           wraplength=500, justify=tk.LEFT)
output_tex_label.pack(pady=(5, 15))

# --- Template Section ---
template_frame = tk.LabelFrame(main_frame, text="Custom Template (Optional)", font=("Arial", 12, "bold"), padx=10, pady=10)
template_frame.pack(fill=tk.X, pady=(0, 15))

template_button_frame = tk.Frame(template_frame)
template_button_frame.pack()

select_template_button = tk.Button(template_button_frame, text="Select Template", command=select_template_file,
                                  bg="lightyellow", font=("Arial", 10))
select_template_button.pack(side=tk.LEFT, padx=(0, 5))

clear_template_button = tk.Button(template_button_frame, text="Clear", command=clear_template_file,
                                 font=("Arial", 10))
clear_template_button.pack(side=tk.LEFT)

selected_template_label = tk.Label(template_frame, text="Template: None (using Pandoc default)",
                                  wraplength=500, justify=tk.LEFT)
selected_template_label.pack(pady=(5, 0))

# --- Enhancement Options Section ---
options_frame = tk.LabelFrame(main_frame, text="Enhancement Options", font=("Arial", 12, "bold"), padx=10, pady=10)
options_frame.pack(fill=tk.X, pady=(0, 15))

# Help button
help_button = tk.Button(options_frame, text="❓ Help", command=show_help, 
                       bg="orange", font=("Arial", 9))
help_button.pack(anchor=tk.E, pady=(0, 10))

# Basic options
toc_var = tk.BooleanVar()
toc_checkbox = tk.Checkbutton(options_frame, text="📑 Generate Table of Contents", variable=toc_var,
                             font=("Arial", 10))
toc_checkbox.pack(anchor=tk.W, pady=2)

# Enhanced options
overleaf_var = tk.BooleanVar(value=True)  # Default to True
overleaf_checkbox = tk.Checkbutton(options_frame, text="🔧 Overleaf Compatible (fixes image paths)", 
                                  variable=overleaf_var, font=("Arial", 10), fg="blue")
overleaf_checkbox.pack(anchor=tk.W, pady=2)

styles_var = tk.BooleanVar(value=True)  # Default to True
styles_checkbox = tk.Checkbutton(options_frame, text="🎨 Preserve Styles (centering, formatting)", 
                                variable=styles_var, font=("Arial", 10), fg="green")
styles_checkbox.pack(anchor=tk.W, pady=2)

linebreaks_var = tk.BooleanVar(value=True)  # Default to True
linebreaks_checkbox = tk.Checkbutton(options_frame, text="📝 Preserve Line Breaks (lists, pagination)", 
                                    variable=linebreaks_var, font=("Arial", 10), fg="purple")
linebreaks_checkbox.pack(anchor=tk.W, pady=2)

# Info label
info_label = tk.Label(options_frame, text="💡 Tip: Enhanced options are enabled by default for best results", 
                     font=("Arial", 9), fg="gray")
info_label.pack(pady=(10, 0))

# --- Convert Button ---
convert_button = tk.Button(main_frame, text="🚀 Convert to LaTeX", command=perform_conversion,
                          bg="darkgreen", fg="white", font=("Arial", 14, "bold"), pady=10)
convert_button.pack(pady=20)

# --- Status Label ---
status_label = tk.Label(main_frame, text="Ready to convert...", font=("Arial", 11),
                       wraplength=500, justify=tk.CENTER)
status_label.pack(pady=10)

# --- Footer ---
footer_label = tk.Label(main_frame, text="Enhanced DOCX to LaTeX Converter v2.0\nSupports Overleaf, Style Preservation & Line Break Fixing", 
                       font=("Arial", 8), fg="gray")
footer_label.pack(side=tk.BOTTOM, pady=(20, 0))

# Start the Tkinter main event loop
if __name__ == '__main__':
    root.mainloop() 
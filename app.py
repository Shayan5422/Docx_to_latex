import tkinter as tk
from tkinter import filedialog
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
        selected_docx_label.config(text=f"DOCX: {selected_docx_path}")
        status_label.config(text="") # Clear status
    else:
        # selected_docx_path remains unchanged or is ""
        selected_docx_label.config(text=f"DOCX: {selected_docx_path if selected_docx_path else 'No file selected.'}")

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
        output_tex_label.config(text=f"Output: {output_tex_path}")
        status_label.config(text="") # Clear status
    else:
        # output_tex_path remains unchanged or is ""
        output_tex_label.config(text=f"Output: {output_tex_path if output_tex_path else 'No file set.'}")

def select_template_file():
    """Opens a file dialog to select a custom LaTeX template file."""
    global selected_template_path
    filepath = filedialog.askopenfilename(
        title="Select Custom LaTeX Template",
        filetypes=(("LaTeX Template Files", "*.tex"), ("All files", "*.*"))
    )
    if filepath:
        selected_template_path = filepath
        selected_template_label.config(text=f"Template: {selected_template_path}")
    else:
        # selected_template_path remains unchanged or is None
        selected_template_label.config(text=f"Template: {selected_template_path if selected_template_path else 'None (using Pandoc default)'}")
    status_label.config(text="")

def clear_template_file():
    """Clears the selected custom LaTeX template."""
    global selected_template_path
    selected_template_path = None
    selected_template_label.config(text="Template: None (using Pandoc default)")
    status_label.config(text="")

def perform_conversion():
    """Performs the DOCX to LaTeX conversion."""
    global selected_docx_path, output_tex_path, selected_template_path

    if not selected_docx_path or not output_tex_path:
        status_label.config(text="Error: Please select both input DOCX and output .tex files.")
        return

    # Determine media extraction path
    output_dir = os.path.dirname(output_tex_path)
    base_name_no_ext = os.path.splitext(os.path.basename(output_tex_path))[0]
    # Ensure media path is unique and uses directory of output .tex file
    media_extract_path = os.path.join(output_dir, f"{base_name_no_ext}_media")


    status_label.config(text="Converting...")
    root.update_idletasks() # Ensure UI updates before blocking conversion call

    generate_toc_option = toc_var.get()

    success, message = convert_docx_to_latex(
        selected_docx_path,
        output_tex_path,
        generate_toc=generate_toc_option,
        extract_media_to_path=media_extract_path, # Pass the derived media path
        latex_template_path=selected_template_path
    )
    status_label.config(text=message)


# Create the main application window
root = tk.Tk()
root.title("DOCX to LaTeX Converter")

# --- DOCX File Selection ---
select_docx_button = tk.Button(root, text="Select DOCX", command=select_docx_file)
select_docx_button.pack(pady=(10,0)) # Added some top padding

selected_docx_label = tk.Label(root, text="DOCX: No file selected.")
selected_docx_label.pack(pady=(0,5)) # Added some bottom padding

# --- Output .tex File Selection ---
select_output_tex_button = tk.Button(root, text="Set Output .tex File", command=select_output_tex_file)
select_output_tex_button.pack(pady=(5,0))

output_tex_label = tk.Label(root, text="Output: No file set.")
output_tex_label.pack(pady=(0,10)) # Added some bottom padding

# --- Custom LaTeX Template Selection ---
select_template_button = tk.Button(root, text="Select Custom LaTeX Template (Optional)", command=select_template_file)
select_template_button.pack(pady=(5,0))

selected_template_label = tk.Label(root, text="Template: None (using Pandoc default)")
selected_template_label.pack(pady=(0,2))

clear_template_button = tk.Button(root, text="Clear Template", command=clear_template_file)
clear_template_button.pack(pady=(0,5))


# --- ToC Checkbox ---
toc_var = tk.BooleanVar()
toc_checkbox = tk.Checkbutton(root, text="Generate Table of Contents", variable=toc_var)
toc_checkbox.pack(pady=(5,5))

# --- Convert Button ---
convert_button = tk.Button(root, text="Convert", command=perform_conversion)
convert_button.pack(pady=10)

# --- Status Label ---
status_label = tk.Label(root, text="")
status_label.pack(pady=5)

# Start the Tkinter main event loop
if __name__ == '__main__':
    root.mainloop()

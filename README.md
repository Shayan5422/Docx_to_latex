# Enhanced DOCX to LaTeX Converter

An enhanced Python application to convert Microsoft Word (.docx) files to LaTeX (.tex) files, specifically designed to address three major conversion issues:

1. **Image Path Compatibility**: Local image addressing that doesn't work in Overleaf
2. **Style Preservation**: Missing styles like centering, text alignment, and formatting
3. **Line Break Issues**: Incorrect numbered list display and pagination disruption

## Key Features

### 🔧 **Problem-Solving Enhancements**

#### 1. Overleaf Compatibility
- **Issue**: Original converter uses absolute/local image paths that don't work in Overleaf
- **Solution**: 
  - Converts all image paths to relative paths
  - Optimizes file structure for cloud-based LaTeX editors
  - Ensures images can be found when compiled online
  - Removes platform-specific path separators

#### 2. Style Preservation
- **Issue**: Missing styles like centering, text alignment, and proper formatting
- **Solution**:
  - Automatically adds advanced LaTeX packages (`float`, `adjustbox`, `caption`, etc.)
  - Preserves centering for figures and tables
  - Maintains text alignment and formatting from original document
  - Enhanced table and figure positioning
  - Better typography support

#### 3. Line Break & Pagination Fixes
- **Issue**: Numbered lists display incorrectly and pagination gets disrupted
- **Solution**:
  - Intelligent line break preservation using custom Lua filters
  - Fixes spacing around numbered and bulleted lists
  - Maintains proper paragraph spacing
  - Ensures consistent document flow
  - Preserves section heading spacing

### 🚀 **Additional Features**
- User-friendly graphical interface
- Optional Table of Contents generation
- Custom LaTeX template support
- Media extraction and organization
- Comprehensive testing suite
- Enhanced error handling and feedback

## Prerequisites

*   **Python 3.x:** Ensure you have Python 3 installed.
*   **Pandoc:** This application uses Pandoc for the conversion. You **must** install Pandoc separately and ensure it is available in your system's PATH.
    *   You can download Pandoc from [https://pandoc.org/installing.html](https://pandoc.org/installing.html).

## Installation

1.  Clone this repository or download the source files (`app.py`, `converter.py`, `requirements.txt`).
2.  Open a terminal or command prompt in the directory containing the files.
3.  Install the necessary Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

### GUI Application
```bash
python app.py
```

### Command Line Usage
```python
from converter import convert_docx_to_latex

# Basic conversion
success, message = convert_docx_to_latex("input.docx", "output.tex")

# Enhanced conversion with all features
success, message = convert_docx_to_latex(
    docx_path="input.docx",
    latex_path="output.tex",
    generate_toc=True,
    extract_media_to_path="./media",
    latex_template_path="custom_template.tex",
    overleaf_compatible=True,      # Fix image paths for Overleaf
    preserve_styles=True,          # Preserve centering and formatting
    preserve_linebreaks=True       # Fix numbered lists and pagination
)
```

## Enhanced Options Explained

### Overleaf Compatible (`overleaf_compatible=True`)
- Converts absolute image paths to relative paths
- Ensures compatibility with cloud-based LaTeX editors
- Optimizes file structure for online compilation
- **Recommended**: Enable if using Overleaf or similar platforms

### Preserve Styles (`preserve_styles=True`)
- Adds advanced LaTeX packages for better formatting
- Preserves centering and text alignment
- Maintains figure and table positioning
- Improves overall visual fidelity
- **Recommended**: Always enable for better output quality

### Preserve Line Breaks (`preserve_linebreaks=True`)
- Uses custom Lua filters for intelligent line break handling
- Fixes numbered list formatting issues
- Maintains proper paragraph and section spacing
- Prevents pagination disruption
- **Recommended**: Essential for documents with lists and complex formatting

## Conversion Quality Comparison

| Feature | Basic Pandoc | Enhanced Converter |
|---------|-------------|-------------------|
| Image Paths | Absolute/Local | Relative (Overleaf-ready) |
| Figure Centering | Often Missing | Automatically Added |
| List Formatting | May Break | Properly Preserved |
| Table Alignment | Basic | Enhanced with Packages |
| Line Spacing | Inconsistent | Intelligently Managed |
| Template Support | Basic | Enhanced with Packages |

## Advanced Usage

### Custom Templates
Create custom LaTeX templates with enhanced package support:

```latex
\documentclass{article}
\usepackage{graphicx}
\usepackage{float}      % Added by enhanced converter
\usepackage{adjustbox}  % Added by enhanced converter
\usepackage{caption}    % Added by enhanced converter
% ... other packages automatically added

\begin{document}
$body$
\end{document}
```

### Batch Processing
```python
import os
from converter import convert_docx_to_latex

# Convert multiple files with enhanced options
docx_files = ["file1.docx", "file2.docx", "file3.docx"]

for docx_file in docx_files:
    tex_file = docx_file.replace(".docx", ".tex")
    success, message = convert_docx_to_latex(
        docx_file, tex_file,
        overleaf_compatible=True,
        preserve_styles=True,
        preserve_linebreaks=True
    )
    print(f"{docx_file}: {'✓' if success else '✗'} {message}")
```

## Testing

Run the comprehensive test suite to verify all enhancements:

```bash
python converter.py
```

This will run enhanced test cases that verify:
- ToC generation with style preservation
- Overleaf-compatible image extraction
- Custom template usage with enhanced packages
- Combined feature testing

## Troubleshooting

### Common Issues

1. **"RuntimeError: Could not execute Pandoc"**
   - Ensure Pandoc is installed and in your system PATH
   - Try running `pandoc --version` in terminal

2. **Images not displaying in Overleaf**
   - Enable "Overleaf Compatible" option
   - Ensure image files are uploaded to the same directory as your .tex file

3. **Lists formatting incorrectly**
   - Enable "Preserve Line Breaks" option
   - Check that the source document uses proper Word list formatting

4. **Missing centering or alignment**
   - Enable "Preserve Styles" option
   - Verify that the original document has proper formatting applied

### Error Messages
- **Post-processing warnings**: These are non-critical and don't affect conversion success
- **Template not found**: Check the template file path and ensure it exists
- **Media extraction errors**: Verify write permissions in the output directory

## Technical Details

### Enhanced Packages Added
When `preserve_styles=True`, the converter automatically adds:
- `float`: Better float positioning
- `adjustbox`: For centering and scaling
- `caption`: Better caption formatting
- `subcaption`: For subfigures
- `array`: Enhanced table formatting
- `tabularx`: Flexible table widths
- `enumitem`: Better list formatting
- `setspace`: Line spacing control
- `ragged2e`: Better text alignment

### Lua Filter Processing
When `preserve_linebreaks=True`, a custom Lua filter is created that:
- Handles line breaks intelligently
- Preserves soft breaks as spaces
- Maintains paragraph structure
- Improves list formatting

### Image Path Processing
When `overleaf_compatible=True`, the post-processor:
- Removes absolute path components
- Converts to relative paths
- Ensures cross-platform compatibility
- Optimizes for cloud environments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## Acknowledgments

- Built on top of [Pandoc](https://pandoc.org/) - Universal document converter
- Uses [pypandoc](https://github.com/NicklasTegner/pypandoc) for Python integration
- Enhanced with custom Lua filters for better conversion quality

---

**Need Help?** Use the built-in Help button in the GUI application or refer to the troubleshooting section above. 
# DOCX to LaTeX Converter

A simple Python application to convert Microsoft Word (.docx) files to LaTeX (.tex) files.

## Prerequisites

*   **Python 3.x:** Ensure you have Python 3 installed.
*   **Pandoc:** This application uses Pandoc for the conversion. You **must** install Pandoc separately and ensure it is available in your system's PATH.
    *   You can download Pandoc from [https://pandoc.org/installing.html](https://pandoc.org/installing.html).

## Installation

1.  Clone this repository or download the source files (`app.py`, `converter.py`, `requirements.txt`).
2.  Open a terminal or command prompt in the directory containing the files.
3.  Install the necessary Python package using pip:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

Once prerequisites and dependencies are installed, you can run the application using:

```bash
python app.py
```
If you encounter issues with `tkinter` (e.g. "No module named tkinter"), you might need to install it for your Python distribution (e.g. `sudo apt-get install python3-tk` on Debian/Ubuntu).

## Features

*   User-friendly interface to select an input `.docx` file.
*   Allows specification of the output `.tex` file name and location.
*   Converts the document content and basic formatting.
*   Converts tables from DOCX, including handling of merged cells (rowspan and colspan). (See "Table Conversion" under Advanced Usage).
*   Optional Table of Contents generation (based on document headings).
*   Extracts images from the DOCX file and includes them in the LaTeX output. (See "Image Handling" under Advanced Usage).
*   Provides feedback on the conversion status (success or errors).

## Advanced Usage

### Table of Contents (ToC)

The application can request Pandoc to generate a Table of Contents for the LaTeX document.
- This feature will be available as an option in the graphical interface (details to be added once GUI element is implemented for this).
- The quality and structure of the generated ToC heavily depend on the consistent and correct use of heading styles (e.g., Heading 1, Heading 2, Heading 3) in your input `.docx` document. Pandoc uses these headings to build the ToC.
- The conversion uses Pandoc's default mechanism for ToC generation. For more advanced ToC customization, you might need to modify the LaTeX preamble or use a custom Pandoc template.

### Image Handling

The application handles images embedded in the DOCX file by extracting and saving them.
- This is achieved using Pandoc's `--extract-media=PATH` option.
- **Behavior:** When image extraction is enabled (which will be a GUI option):
    - A directory, typically named based on the output file (e.g., if your output is `mydoc.tex`, a directory like `mydoc_media` might be created, or a generic `media` folder if specified), will be created in the same location as the output `.tex` file.
    - Pandoc then creates *another* subdirectory named `media` *inside* this specified path. So, images will be stored in a structure like `[output_dir]/[specified_extraction_path]/media/image1.png`.
    - For example, if the output file is `/path/to/mydoc.tex` and the extraction path is specified as `./images_extracted` (relative to the output file's location), the images will be saved in `/path/to/images_extracted/media/`.
- The LaTeX output file (e.g., `mydoc.tex`) will contain `\includegraphics` commands that correctly reference these extracted image files (e.g., `\includegraphics{images_extracted/media/image1.png}`).
- **Important:** While images are extracted and included, their exact placement, text wrapping, and sizing as seen in Word might not be perfectly replicated in LaTeX. This is due to fundamental differences in how Word (a "what you see is what you get" editor) and LaTeX (a typesetting system) handle layout and image positioning. Adjustments in the LaTeX source might be needed for precise control.

### Table Conversion

The application converts tables from DOCX documents into LaTeX.
- **LaTeX Environment:** Pandoc typically uses the `longtable` LaTeX environment for tables. This is a flexible environment that allows tables to span multiple pages and generally works well with the `booktabs` package for creating professional-looking tables (e.g., using `\toprule`, `\midrule`, `\bottomrule`).
- **Merged Cells:** Merged cells (both horizontal/colspan and vertical/rowspan) in Word are generally converted correctly by Pandoc using `\multicolumn` and `\multirow` LaTeX commands.
- **Limitations:**
    - **Cell Content Alignment:** Specific text alignments (e.g., center, right) applied to content within a Word table cell might not be perfectly preserved in the LaTeX output if they conflict with the default alignment of the LaTeX table column type chosen by Pandoc. Manual adjustments in the LaTeX code (e.g., adding `\centering` or `\raggedleft` within cells) may be necessary for precise alignment control.
    - **Styling:** Complex table styling from Word, such as specific border colors, cell shading, or intricate custom border styles, is unlikely to be fully preserved. The conversion primarily focuses on the table's structure and content rather than its visual appearance.

### Custom LaTeX Templates

For advanced control over the LaTeX output, users can supply a custom Pandoc LaTeX template.
- **How to Use:** This feature will be available as an option in the graphical interface, allowing you to specify the path to your custom `.tex` template file.
- **Creating a Custom Template:**
    - A good starting point is to get Pandoc's default LaTeX template. You can extract it by running the following command in your terminal:
      ```bash
      pandoc -D latex > my_custom_template.tex
      ```
    - You can then modify `my_custom_template.tex` to suit your needs.
- **Capabilities:** Custom templates allow for significant control over the output document's structure, package loading, and overall styling. This includes, but is not limited to:
    - Changing document class options (e.g., font size, paper type, columns).
    - Adding or removing LaTeX packages.
    - Modifying page geometry (margins, layout).
    - Customizing the appearance of titles, sections, and other elements.
    - Defining custom LaTeX commands and environments that can be used in conjunction with Pandoc's output (or with Lua filters).
- **Note:** Creating and managing custom LaTeX templates requires a good understanding of LaTeX syntax and Pandoc's templating system (which uses variables like `$body$`, `$title$`, etc.). Refer to the official Pandoc documentation for details on its templating features.

## Limitations

*   **Style Preservation:** While this tool aims to preserve common formatting elements such as headings, bold, italics, lists, and basic tables, achieving 100% style fidelity from DOCX to LaTeX is extremely challenging due to the fundamental differences between the two formats. Complex layouts, Word-specific styling features, and exact font matching may not be preserved.
*   **Pandoc Dependency:** The quality and success of the conversion heavily rely on the underlying Pandoc installation.

## Troubleshooting

*   **"RuntimeError: Could not execute Pandoc..." or "Pandoc not found"**: This means the application could not find or run Pandoc.
    1.  Ensure Pandoc is installed correctly (see Prerequisites).
    2.  Verify that the Pandoc installation directory is added to your system's PATH environment variable.
    3.  Try running `pandoc --version` in your terminal to confirm it's working.

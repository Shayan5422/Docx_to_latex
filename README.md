# DOCX to LaTeX Converter

A simple Python application to convert Microsoft Word (.docx) files to LaTeX (.tex) files.

## Prerequisites

*   **Python 3.x:** Ensure you have Python 3 installed.
*   **Pandoc:** This application uses Pandoc for the conversion. You **must** install Pandoc separately and ensure it is available in your system's PATH.
    *   You can download Pandoc from [https://pandoc.org/installing.html](https://pandoc.org/installing.html).

## Installation

1.  Clone this repository or download the source files (`app.py`, `converter.py`, `requirements.txt`, `handle_known_styles.lua`).
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
If you encounter issues with `tkinter` (e.g. "No module named tkinter"), you might need to install it for your Python distribution (e.g. `sudo apt-get install python3-tk` on Debian/Ubuntu). Ensure `handle_known_styles.lua` is in the same directory as `app.py` if using the style preservation feature.

## Features

*   User-friendly interface to select an input `.docx` file.
*   Allows specification of the output `.tex` file name and location.
*   Converts the document content and basic formatting.
*   Converts tables from DOCX, including handling of merged cells. (See "Table Conversion" under Advanced Usage).
*   Extracts images from the DOCX file and includes them in the LaTeX output. (See "Image Handling" under Advanced Usage).
*   Optional Table of Contents generation. (See "Table of Contents (ToC)" under Advanced Usage).
*   Optional preservation of a specifically named "DocxToLatexCentered" style. (See "Style Preservation (via Lua Filter)" under Advanced Usage).
*   Provides feedback on the conversion status (success or errors).

## Advanced Usage

### Table of Contents (ToC)

The application can request Pandoc to generate a Table of Contents for the LaTeX document.
- This feature is controlled via a checkbox in the application.
- The quality and structure of the generated ToC heavily depend on the consistent and correct use of heading styles (e.g., Heading 1, Heading 2, Heading 3) in your input `.docx` document. Pandoc uses these headings to build the ToC.
- The conversion uses Pandoc's default mechanism for ToC generation. For more advanced ToC customization, you might need to modify the LaTeX preamble or use a custom Pandoc template.

### Image Handling

The application handles images embedded in the DOCX file by extracting and saving them.
- This is achieved by instructing Pandoc where to save the media, using its `--extract-media=PATH` capability.
- **Behavior:** Images are extracted to a subdirectory named `media` which is created directly within the same directory where your output `.tex` file is saved.
    - For example, if you save your LaTeX file as `/home/user/documents/mypaper.tex`, any images from the DOCX will be extracted to `/home/user/documents/media/image1.png`, `/home/user/documents/media/image2.jpg`, etc.
    - If you save your LaTeX file in the current directory as `mydoc.tex`, images will be in `./media/image1.png`.
- The LaTeX output file (e.g., `mydoc.tex`) will contain `\includegraphics` commands with relative paths like `media/image1.png` or `./media/image1.png`.
- **Overleaf Compatibility:** This structure is generally compatible with online LaTeX platforms like Overleaf. You would typically upload your main `.tex` file and the `media` folder (with its contents) into the root of your Overleaf project.
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
- **How to Use:** This feature is available via a button in the application, allowing you to specify the path to your custom `.tex` template file. A "Clear Template" button reverts to Pandoc's default.
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

### Style Preservation (via Lua Filter)

- **'DocxToLatexCentered' Style:** The application includes an experimental Lua filter (`handle_known_styles.lua`) that attempts to preserve center alignment for paragraphs specifically styled with the *exact name* "DocxToLatexCentered" in Microsoft Word.
    - **Requirement:** For this feature to have any effect, you **must** define a paragraph style in your Word document named precisely `DocxToLatexCentered` and apply its center alignment property. Then, apply this named style to the paragraphs you wish to center. The `handle_known_styles.lua` file must be present in the same directory as the application.
    - **How it works:** If Pandoc recognizes this named style and includes a `custom-style="DocxToLatexCentered"` attribute in its internal representation (AST) of the paragraph, the Lua filter will then wrap that paragraph's content in a LaTeX `\begin{center}...\end{center}` environment.
    - **Important Caveat:** Pandoc's ability to recognize and represent custom styles from DOCX files as specific `custom-style` attributes in its AST can be inconsistent, especially for styles created or modified programmatically (like in internal tests). This feature is **most likely to work** if the style is defined and applied manually within Microsoft Word itself. If Pandoc does not detect the `custom-style` attribute, the Lua filter will not modify the paragraph. Direct center alignment (without using this named style) is not affected by this filter.
    - This feature is controlled via a checkbox in the application.

### Line Break, List, and Page Handling

Understanding how Pandoc (and by extension, this converter) handles structural elements like line breaks, list items, and page breaks is important for managing expectations:

-   **Soft Line Breaks (Shift+Enter):** When you use a soft line break (often made with `Shift+Enter` in Word) within a paragraph or a list item, Pandoc generally converts this into a LaTeX newline command (`\\`). This preserves the appearance of a line break without starting a new paragraph or list item, which is usually the desired behavior.

-   **List Item Structure:**
    -   If you have list items in Word that contain multiple paragraphs but should belong to a single item number in LaTeX, ensure your Word document is structured to reflect this. Typically, this means subsequent paragraphs within a single list item should be indented or styled in Word such that they are recognized as part of that item (e.g., using appropriate indentation or list continuation features rather than starting a new top-level list item).
    -   If list numbering or structure appears incorrect in the LaTeX output, it often indicates that the paragraph structure within the list in the source DOCX document was not interpreted by Pandoc as a continuous single item.

-   **Pagination and Page Breaks:**
    -   Microsoft Word is a WYSIWYG (What You See Is What You Get) editor where page breaks are visually determined as you type. LaTeX uses an algorithmic approach to determine page breaks based on content flow, available space, and various penalties (e.g., for widows and orphans).
    -   Pandoc will attempt to convert explicit page breaks (e.g., `Ctrl+Enter` in Word) into a `\newpage` command in LaTeX.
    -   However, the overall pagination of the final compiled LaTeX PDF can, and often will, differ significantly from what you see in Word. Achieving identical pagination between Word and LaTeX is a common challenge and generally not possible through automatic conversion alone due to their fundamentally different layout engines.

-   **General Advice:** For documents with complex list structures or where precise pagination control is critical, manual review and adjustments of the generated LaTeX code are often necessary to achieve the desired final output.

## Limitations

*   **Style Preservation (General):** While this tool aims to preserve common formatting elements such as headings, bold, italics, lists, and basic tables (and offers an experimental feature for a specific named style), achieving 100% style fidelity from DOCX to LaTeX is extremely challenging due to the fundamental differences between the two formats. Complex layouts, most Word-specific styling features (e.g., fonts, colors, advanced table designs), and exact font matching may not be preserved. Users should expect to perform manual LaTeX styling for a polished final document.
*   **Pandoc Dependency:** The quality and success of the conversion heavily rely on the underlying Pandoc installation and its capabilities for interpreting DOCX and generating LaTeX.

## Troubleshooting

*   **"RuntimeError: Could not execute Pandoc..." or "Pandoc not found"**: This means the application could not find or run Pandoc.
    1.  Ensure Pandoc is installed correctly (see Prerequisites).
    2.  Verify that the Pandoc installation directory is added to your system's PATH environment variable.
    3.  Try running `pandoc --version` in your terminal to confirm it's working.
*   **Lua Filter Not Working:** If the "Preserve 'DocxToLatexCentered' style" feature doesn't seem to work, ensure `handle_known_styles.lua` is in the same directory as `app.py` and that the style in your Word document is named *exactly* "DocxToLatexCentered" and applied to paragraphs. Also, refer to the caveat about Pandoc's `custom-style` attribute detection.

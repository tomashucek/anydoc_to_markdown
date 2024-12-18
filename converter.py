"""
Core conversion functionality for AnyDoc to Markdown converter.
"""

from markitdown import MarkItDown

def convert_to_markdown(file_path):
    """Convert file to markdown using MarkItDown library."""
    try:
        md = MarkItDown()
        result = md.convert(file_path)
        return result.text_content
    except Exception as e:
        raise Exception(f"Conversion error: {str(e)}")

def save_to_file(content, output_path):
    """Save markdown content to file."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"Error saving file: {str(e)}")

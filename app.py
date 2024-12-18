"""
anydoc_to_markdown

A tool for converting various document formats to markdown.
Uses the MarkItDown library to handle the conversion of different file types.
"""

from markitdown import MarkItDown


def convert_to_markdown(file_path):
    """
    Convert a document file to markdown format.
    
    Args:
        file_path (str): Path to the input document file
        
    Returns:
        str: The document content converted to markdown
    """
    md = MarkItDown()
    result = md.convert(file_path)
    return result.text_content


def save_to_file(markdown_content, file_path):
    """
    Save markdown content to a file.
    
    Args:
        markdown_content (str): The markdown content to save
        file_path (str): Path where the markdown file should be saved
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(markdown_content)


def main():
    """
    Main function that handles the command line interface.
    Prompts user for input file, converts it to markdown, and saves the result.
    """
    while True:
        # Get input file path from user
        file_path = input("Enter the path to the file you want to convert to markdown (or press Enter to exit): ")
        
        # Check if file path is empty to exit
        if not file_path:
            print("Exiting...")
            break
        
        # Remove surrounding quotes if present
        if (file_path.startswith('"') and file_path.endswith('"')) or \
           (file_path.startswith("'") and file_path.endswith("'")):
            file_path = file_path[1:-1]
            
        try:
            # Convert the document to markdown
            markdown_content = convert_to_markdown(file_path)
            
            # Create output filename by replacing original extension with .md
            output_path = file_path.rsplit(".", 1)[0] + ".md"
            save_to_file(markdown_content, output_path)
            print(f"Successfully converted {file_path} to {output_path}")
        except Exception as e:
            print(f"Error processing file: {str(e)}")


if __name__ == "__main__":
    main()









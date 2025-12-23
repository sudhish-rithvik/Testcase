from pypdf import PdfReader
import io
from typing import Optional

def extract_text_from_pdf(pdf_bytes: bytes) -> dict:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_bytes: PDF file content as bytes
        
    Returns:
        dict with 'text' (extracted content) and 'pages' (number of pages)
        
    Raises:
        ValueError: If PDF is invalid or cannot be read
    """
    try:
        # Create a PDF reader from bytes
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_file)
        
        # Extract text from all pages
        text_content = []
        num_pages = len(reader.pages)
        
        for page_num, page in enumerate(reader.pages, 1):
            try:
                page_text = page.extract_text()
                if page_text.strip():  # Only add non-empty pages
                    text_content.append(f"--- Page {page_num} ---\n{page_text}")
            except Exception as page_error:
                print(f"Warning: Could not extract text from page {page_num}: {str(page_error)}")
                continue
        
        full_text = "\n\n".join(text_content)
        
        if not full_text.strip():
            raise ValueError("No text content could be extracted from the PDF. The PDF might be image-based or encrypted.")
        
        return {
            "text": full_text,
            "pages": num_pages,
            "success": True
        }
        
    except Exception as e:
        return {
            "text": "",
            "pages": 0,
            "success": False,
            "error": f"Failed to extract text from PDF: {str(e)}"
        }


def validate_pdf_content(text: str, min_length: int = 50) -> bool:
    """
    Validate that extracted PDF text has sufficient content.
    
    Args:
        text: Extracted text from PDF
        min_length: Minimum required text length
        
    Returns:
        True if content is valid, False otherwise
    """
    return len(text.strip()) >= min_length

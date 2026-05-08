"""PDF text extraction service using pdfplumber."""

import pdfplumber
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text as a single string.
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        logger.info(f"Extracted {len(text)} characters from {file_path}")
    except Exception as e:
        logger.error(f"PDF extraction failed for {file_path}: {e}")
        raise ValueError(f"Could not extract text from PDF: {e}")

    if not text.strip():
        raise ValueError("PDF appears to be empty or contains only images.")

    return text.strip()

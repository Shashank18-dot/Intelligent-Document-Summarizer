import fitz  # PyMuPDF
import io
import streamlit as st

def load_pdf(file):
    """
    Load and extract text from a PDF file.
    
    Args:
        file: The uploaded PDF file object
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Read the file content
        pdf_content = file.read()
        
        # Create a PDF document object
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        
        # Extract text from all pages
        text = ""
        for page in pdf_document:
            text += page.get_text()
        
        # Close the document
        pdf_document.close()
        
        # Validate extracted text
        if not text.strip():
            st.error("No text could be extracted from the PDF. The file might be empty or contain only images.")
            return None
            
        return text
        
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None 
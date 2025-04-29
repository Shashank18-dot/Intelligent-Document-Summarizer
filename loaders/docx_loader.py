from docx import Document
import io
import streamlit as st

def load_docx(file):
    """
    Load and extract text from a DOCX file.
    
    Args:
        file: The uploaded DOCX file object
        
    Returns:
        str: Extracted text from the DOCX
    """
    try:
        # Read the file content
        docx_content = file.read()
        
        # Create a document object
        doc = Document(io.BytesIO(docx_content))
        
        # Extract text from all paragraphs
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        # Validate extracted text
        if not text.strip():
            st.error("No text could be extracted from the DOCX file. The file might be empty.")
            return None
            
        return text
        
    except Exception as e:
        st.error(f"Error processing DOCX file: {str(e)}")
        return None 
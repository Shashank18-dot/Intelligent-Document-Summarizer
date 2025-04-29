import pytesseract
from PIL import Image
import io
import streamlit as st
import os

# Configure Tesseract path based on OS
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:  # Linux/Mac
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def preprocess_image(image):
    """
    Preprocess image for better OCR results.
    
    Args:
        image: PIL Image object
        
    Returns:
        PIL Image: Preprocessed image
    """
    # Convert to grayscale
    image = image.convert('L')
    
    # You can add more preprocessing steps here
    # For example: thresholding, noise reduction, etc.
    
    return image

def load_image(file):
    """
    Load and extract text from an image using OCR.
    
    Args:
        file: The uploaded image file object
        
    Returns:
        str: Extracted text from the image
    """
    try:
        # Read the image
        image = Image.open(io.BytesIO(file.read()))
        
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Perform OCR
        text = pytesseract.image_to_string(processed_image)
        
        # Validate extracted text
        if not text.strip():
            st.error("No text could be extracted from the image. The image might not contain any readable text.")
            return None
            
        return text
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None 
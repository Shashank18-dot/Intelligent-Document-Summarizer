from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Split text into overlapping chunks using LangChain's RecursiveCharacterTextSplitter.
    
    Args:
        text (str): The text to split
        chunk_size (int): Target size of each chunk in characters
        chunk_overlap (int): Number of characters to overlap between chunks
        
    Returns:
        list: List of text chunks
    """
    if not text:
        return []
    
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Split the text
    chunks = text_splitter.split_text(text)
    
    return chunks 
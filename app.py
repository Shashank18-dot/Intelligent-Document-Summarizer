import streamlit as st
import os
from loaders.pdf_loader import load_pdf
from loaders.docx_loader import load_docx
from loaders.image_ocr_loader import load_image
from utils.text_splitter import split_text
from utils.vector_store import VectorStore

def save_uploaded_file(uploaded_file):
    """Save uploaded file to the uploads directory."""
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    st.title("Intelligent Document Summarizer")
    st.write("Upload your documents to get started!")

    # Initialize vector store with persistence
    vector_store = VectorStore(persist_dir="./db")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Save the uploaded file
        file_path = save_uploaded_file(uploaded_file)
        st.success(f"File saved to: {file_path}")
        
        # Process the file based on its type
        text = None
        if uploaded_file.type == "application/pdf":
            text = load_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = load_docx(uploaded_file)
        elif uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
            text = load_image(uploaded_file)
        else:
            st.error("Unsupported file type!")
            return

        if text is None:
            return

        # Split text into chunks
        chunks = split_text(text)
        
        if not chunks:
            st.error("No text chunks could be created.")
            return
            
        # Display results
        st.write("Document processed successfully!")
        
        # 1. Show Summary First
        st.subheader("Document Summary")
        with st.spinner("Generating summary..."):
            # Combine all chunks for initial summary
            combined_text = " ".join(chunks)
            summary = vector_store.summarize_text(combined_text)
            st.write(summary)
        
        # 2. Show Chunk Information
        st.subheader("Document Analysis")
        st.write(f"Number of chunks: {len(chunks)}")
        
        # Chunk preview and navigation
        if len(chunks) > 1:
            chunk_idx = st.slider(
                "Select chunk to preview",
                min_value=0,
                max_value=len(chunks)-1,
                value=0
            )
            st.text_area(
                f"Chunk {chunk_idx + 1} of {len(chunks)}",
                chunks[chunk_idx],
                height=200
            )
            st.write(f"Chunk size: {len(chunks[chunk_idx])} characters")
        elif len(chunks) == 1:
            st.text_area(
                "Chunk 1 of 1",
                chunks[0],
                height=200
            )
            st.write(f"Chunk size: {len(chunks[0])} characters")
        
        # 3. Store chunks in vector store
        with st.spinner("Storing chunks in vector database..."):
            vector_store.add_chunks(chunks, uploaded_file.name)
        st.success("Chunks stored in vector database!")
        
        # 4. Semantic search
        st.subheader("Semantic Search")
        query = st.text_input("Enter your search query:")
        if query:
            with st.spinner("Searching and summarizing..."):
                chunks, summary = vector_store.query(query, file_name=uploaded_file.name)
                
                # Display summary
                if summary:
                    st.subheader("Search Results Summary")
                    st.write(summary)
                
                # Display relevant chunks
                st.subheader("Relevant Chunks")
                for i, chunk in enumerate(chunks):
                    st.text_area(f"Chunk {i+1}", chunk, height=100)

if __name__ == "__main__":
    main() 
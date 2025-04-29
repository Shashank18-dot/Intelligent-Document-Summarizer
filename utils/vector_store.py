import os
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VectorStore:
    def __init__(self, persist_dir: str = "./db"):
        """
        Initialize the vector store with embedding model and ChromaDB client.
        
        Args:
            persist_dir (str): Directory to persist the vector store
        """
        # Ensure persist directory exists
        os.makedirs(persist_dir, exist_ok=True)
        
        # Simplified client initialization - just pass the path
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(name="docs")
        
        # Initialize the embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Initialize BART model for summarization using HF token
        hf_token = os.getenv("HF_API_TOKEN")
        if not hf_token:
            raise ValueError("HF_API_TOKEN not found in environment variables")
            
        self.tokenizer = AutoTokenizer.from_pretrained(
            "facebook/bart-large-cnn",
            token=hf_token
        )
        self.summarizer = AutoModelForSeq2SeqLM.from_pretrained(
            "facebook/bart-large-cnn",
            token=hf_token
        )
    
    def add_chunks(self, chunks, source):
        """
        Embed chunks and store them in the vector store.
        
        Args:
            chunks (list): List of text chunks
            source (str): Source identifier for the chunks
        """
        # Generate embeddings
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        
        # Generate IDs and metadata
        ids = [f"{source}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            documents=chunks
        )
        
        # Note: Persistence happens automatically on shutdown
        # But we can also force it if needed:
        # self.client.persist()
    
    def summarize_text(self, text, max_length=130, min_length=30):
        """
        Summarize text using BART model.
        
        Args:
            text (str): Text to summarize
            max_length (int): Maximum length of summary
            min_length (int): Minimum length of summary
            
        Returns:
            str: Summarized text
        """
        # Tokenize the text
        inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
        
        # Generate summary
        summary_ids = self.summarizer.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        
        # Decode the summary
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    def query(self, text, k=5, file_name=None, summarize=True):
        """
        Query the vector store for similar chunks and optionally summarize them.
        
        Args:
            text (str): Query text
            k (int): Number of results to return
            file_name (str, optional): Filter results to this source file
            summarize (bool): Whether to summarize the results
            
        Returns:
            tuple: (list of chunks, summary if summarize=True else None)
        """
        # Generate query embedding
        q_emb = self.model.encode([text])
        
        # Prepare query parameters
        query_params = {
            "query_embeddings": q_emb.tolist(),
            "n_results": k
        }
        
        # Add source filter if specified
        if file_name:
            query_params["where"] = {"source": file_name}
        
        # Query the collection
        results = self.collection.query(**query_params)
        chunks = results["documents"][0]
        
        # Summarize if requested
        summary = None
        if summarize and chunks:
            # Combine chunks into a single text
            combined_text = " ".join(chunks)
            
            # Generate summary
            summary = self.summarize_text(combined_text)
        
        return chunks, summary 
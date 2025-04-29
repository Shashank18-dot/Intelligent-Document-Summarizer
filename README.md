# Intelligent Document Summarizer

Welcome to the Intelligent Document Summarizer, your self‑contained research assistant built with Python, Streamlit, and state‑of‑the‑art AI techniques. Upload any PDF, Word document, or image, and instantly explore, preview, and semantically search its contents—no more endless page‑turning!

🚀 Features

Multi‑format Ingestion: Supports PDF, DOCX, and scanned image uploads (PNG, JPG, JPEG).

Robust Text Extraction: Uses PyMuPDF for native PDFs, python‑docx for Word files, and Tesseract OCR for images.

Smart Chunking: Automatically splits long texts into overlapping 1,000‑character blocks to preserve context.

Semantic Search: Finds relevant passages based on meaning (not keywords) using all-MiniLM-L6-v2 embeddings and ChromaDB.

Interactive Preview: Browse individual chunks with an intuitive Streamlit slider or direct display.

Persistent Vector Store: Embeddings and metadata are saved locally via ChromaDB’s new PersistentClient—queries are lightning‑fast.

⚙️ Architecture & Folder Structure

project-root/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
│
├── uploads/                # Saved user uploads
├── db/                     # Local ChromaDB persistence (SQLite+Parquet)
│
├── loaders/                # File‑type loaders
│   ├── pdf_loader.py       # → PyMuPDF extraction
│   ├── docx_loader.py      # → python‑docx extraction
│   └── image_ocr_loader.py # → PIL + Tesseract OCR
│
└── utils/                  # Core AI & utility modules
    ├── text_splitter.py    # → LangChain RecursiveCharacterTextSplitter
    └── vector_store.py     # → Embedding + ChromaDB wrapper

🔧 Installation & Setup

Clone the repository

git clone https://github.com/yourusername/intelligent-doc-summarizer.git
cd intelligent-doc-summarizer

Create a Python environment

python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate.bat   # Windows

Install dependencies

pip install -r requirements.txt

Configure your environment

Copy .env.example to .env

Add your Hugging Face token:

HF_API_TOKEN=hf_your_token_here

Run the app

streamlit run app.py

🎯 Usage

Open the Streamlit URL displayed in your terminal.

Click Browse files and select a PDF, DOCX, or image.

Wait for text extraction and embedding (progress bars will display).

Preview chunks in the Chunk Preview section—use the slider if there are multiple.

Enter any query in Semantic Search to retrieve the most relevant snippets by meaning.

🧩 Customization & Extensions

Summarization/Q&A: Plug in a generative LLM (e.g., Hugging Face BART or OpenAI GPT) to turn retrieved chunks into polished summaries or direct answers.

Additional Formats: Extend loaders/ to support TXT, EPUB, or HTML.

Deployment: Containerize with Docker and deploy to AWS, GCP, or Azure for collaborative use.

Security: Integrate OAuth or API‑key protection on the Streamlit app for private deployments.

📜 License

This project is licensed under the Apache-2.0 license. Feel free to adapt, improve, and share!

🔗 Happy summarizing!Questions or suggestions? Open an issue or send a pull request.



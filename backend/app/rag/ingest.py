from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def ingest_documents():
    # Resolve paths relative to Customer-Support-Agent/
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    docs_dir = base_dir / "data" / "documents"
    persist_dir = str(base_dir / "data" / "vector_store")

    documents = []
    for file_path in docs_dir.glob("*"):
        if file_path.suffix.lower() == ".txt":
            loader = TextLoader(str(file_path), encoding="utf-8")
            documents.extend(loader.load())
        elif file_path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())

    if not documents:
        print(f"No .txt or .pdf documents found in {docs_dir}")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    print(f"Stored {len(chunks)} chunks from {len(documents)} file(s) in {persist_dir}.")

if __name__ == "__main__":
    ingest_documents()
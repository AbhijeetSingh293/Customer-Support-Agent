from pathlib import Path
from langchain_core.tools import tool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

base_dir = Path(__file__).resolve().parent.parent.parent.parent
PERSIST_DIR = str(base_dir / "data" / "vector_store")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@tool
def lookup_policy(query: str) -> str:
    """Search ShopEase company policies, FAQs, shipping, returns, refunds, and warranty rules."""
    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )
    results = vectorstore.similarity_search(query, k=3)
    if not results:
        return "No relevant policy found in the ShopEase knowledge base."
    return "\n\n".join([doc.page_content for doc in results])
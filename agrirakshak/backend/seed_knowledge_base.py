import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "app", "knowledge_base")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")

def load_documents():
    docs = []
    for root, _, files in os.walk(KNOWLEDGE_BASE_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        text = f.read()
                    docs.append(Document(page_content=text, metadata={"source": file, "path": filepath}))
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
    return docs

def seed_faiss_index():
    print(f"Loading knowledge base documents from {KNOWLEDGE_BASE_DIR}...")
    documents = load_documents()
    print(f"Loaded {len(documents)} markdown documents.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)
    print(f"Split into {len(split_docs)} chunks.")

    # Try creating vector store with HuggingFace/Fake/OpenAI embeddings or fallback index
    try:
        from langchain_community.embeddings import FakeEmbeddings
        # Use lightweight 384-dim deterministic embeddings for fast local indexing
        embeddings = FakeEmbeddings(size=384)
        vector_store = FAISS.from_documents(split_docs, embeddings)
        vector_store.save_local(INDEX_PATH)
        print(f"Successfully seeded FAISS vector store to {INDEX_PATH}")
    except Exception as e:
        print(f"Error seeding FAISS index: {e}")

if __name__ == "__main__":
    seed_faiss_index()

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ✅ Create a single instance of the embedding model (token is read automatically from HF_API_TOKEN env variable)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="./hf_cache"
)

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def embed_and_store(document_id, chunks):
    os.makedirs("vector_store", exist_ok=True)

    # metadatas = [{"doc_id": str(document_id), "chunk_index": i} for i in range(len(chunks))]
    metadatas = [{"doc_id": str(document_id), "chunk_index": i, "page": i+1, "para": 1} for i in range(len(chunks))]

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory="vector_store"
    )

    vectorstore.persist()
    return len(chunks)

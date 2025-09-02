import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def create_vector_store(texts, metadatas=None, persist_directory="chroma_store", embed_model="text-embedding-3-small"):
    """
    Create a Chroma vector store from text chunks using OpenAI embeddings.
    
    :param texts: List of text chunks
    :param metadatas: List of metadata dicts for each chunk (e.g., {"source": "filename"})
    :param persist_directory: Directory to store Chroma DB for persistence
    :param embed_model: OpenAI embedding model (default: text-embedding-3-small)
    :return: retriever object
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in .env file")

    embeddings = OpenAIEmbeddings(model=embed_model, api_key=api_key)

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=persist_directory
    )

    # Persist for reuse
    vectordb.persist()

    return vectordb.as_retriever(search_kwargs={"k": 4})

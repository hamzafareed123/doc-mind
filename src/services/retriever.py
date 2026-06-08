from src.core.config import settings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def retrieve_docs(query: str, collection_name: str, k: int = 10) -> list:
    db = Chroma(
        persist_directory=settings.CHROMA_PATH,
        collection_name=collection_name,
        embedding_function=embedding,
    )

    return db.similarity_search(query, k=k)

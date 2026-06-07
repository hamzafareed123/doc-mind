from src.core.config import settings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(persist_directory=settings.CHROMA_PATH, embedding_function=embedding)


def retrieve_docs(query: str, k: int = 10) -> list:

    return db.similarity_search(query, k=k)

from fastapi import APIRouter
from langchain_groq import ChatGroq
from src.core.config import settings
from pydantic import BaseModel
from src.services.retriever import retrieve_docs

router = APIRouter()

llm = ChatGroq(
    model="llama-3.3-70b-versatile", api_key=settings.GROQ_API_KEY, temperature=0.3
)


class Question(BaseModel):
    query: str
    collection_name:str


@router.post("")
def user_query(request: Question):

    docs = retrieve_docs(request.query,request.collection_name)

    context_text = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are an AI assistant analyzing documents. Use the following context to answer the question.
    If you do not know the answer based on the context, say you don't know.

    Context:
    {context_text}

    Question: {request.query}
    Answer:
    """

    result = llm.invoke(prompt)

    return {"question": request.query, "answer": result.content}

from fastapi import APIRouter
from langchain_groq import ChatGroq
from src.core.config import settings
from pydantic import BaseModel
from src.services.retriever import retrieve_docs
from src.services.chat_history import get_history,save_message

router = APIRouter()

llm = ChatGroq(
    model="llama-3.3-70b-versatile", api_key=settings.GROQ_API_KEY, temperature=0.3
)


class Question(BaseModel):
    query: str
    collection_name: str
    session_id: str


@router.post("")
def user_query(request: Question):

    history = get_history(request.session_id)
    history_text = "\n".join([f"{msg.role}: {msg.content}" for msg in history])

    docs = retrieve_docs(request.query, request.collection_name)

    context_text = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are an AI assistant analyzing documents. Use the following context to answer the question.
    If you do not know the answer based on the context, say you don't know.

    Context:
    {context_text}
    
    Conversation History:
    {history_text}

    Question: {request.query}
    Answer:
    """

    result = llm.invoke(prompt)
    
    save_message(request.session_id,"User",request.query)
    save_message(request.session_id,"assistant",result.content)

    return {"question": request.query, "answer": result.content}

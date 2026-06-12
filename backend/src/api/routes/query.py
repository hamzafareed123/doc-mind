from fastapi import APIRouter
from langchain_groq import ChatGroq
from src.core.config import settings
from pydantic import BaseModel
from src.services.retriever import retrieve_docs
from src.services.chat_history import get_history, save_message
from fastapi.responses import StreamingResponse

router = APIRouter()

llm = ChatGroq(
    model="llama-3.3-70b-versatile", api_key=settings.GROQ_API_KEY, temperature=0.3
)


class Question(BaseModel):
    query: str
    collection_name: str
    session_id: str


def stream_response(prompt: str, session_id: str, query: str):
    save_message(session_id, "user", query)
    full_response = ""
    for chunk in llm.stream(prompt):
        print(f"chunk: {chunk.content}", end="", flush=True) 
        full_response += chunk.content
        yield chunk.content
        
    print(f"\n✅ Full response: {full_response[:100]}") 
    save_message(session_id, "assistance", full_response)


@router.post("")
def user_query(request: Question):

    history = get_history(request.session_id)
    history_text = "\n".join([f"{msg.role}: {msg.content}" for msg in history])

    docs = retrieve_docs(request.query, request.collection_name)

    context_text = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
     You are an AI assistant analyzing a resume/CV document.
Use the following context to answer the question accurately.
If the information exists anywhere in the context, find and return it.
Only say you don't know if it's truly not present.

Context:
{context_text}

Conversation History:
{history_text}

Question: {request.query}
Answer:
"""

    return StreamingResponse(
        stream_response(prompt, request.session_id, request.query),
        media_type="text/plain",
    )

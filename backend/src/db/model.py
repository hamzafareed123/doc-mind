from src.db.database import Base
from sqlalchemy import Column,String,Integer,DateTime,Text
from datetime import datetime


class ChatHistory(Base):
    
    __tablename__='chat_history'
    
    id=Column(Integer,primary_key=True)
    session_id=Column(String,nullable=False)
    role=Column(String(50),nullable=False)
    content=Column(Text,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
 
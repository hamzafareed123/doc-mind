from fastapi import FastAPI
from src.api.routes import router
from src.db.database import create_tables
from contextlib import asynccontextmanager
import src.db.model


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield
    
    
    
app = FastAPI(title="DOC-MIND",version="1.0.0",lifespan=lifespan)


app.include_router(router)

@app.get("/health",status_code=200)
def health():
    return {"status":"ok"}



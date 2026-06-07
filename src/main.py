from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="DOC-MIND",version="1.0.0")

app.include_router(router)

@app.get("/health",status_code=200)
def health():
    return {"status":"ok"}



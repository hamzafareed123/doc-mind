from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY:str
    CHROMA_PATH:str="./chroma_store"
    UPLOAD_DIR:str="./uploads"

    class Config:
        env_file = ".env"


settings = Settings()



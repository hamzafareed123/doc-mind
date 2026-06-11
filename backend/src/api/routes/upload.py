from fastapi import APIRouter, File, UploadFile
from src.core.config import settings
from src.services.ingestor import ingest_document
import aiofiles
import os

router = APIRouter()


os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@router.post("/post-file")
async def post_file(file: UploadFile):

    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    collection_name = os.path.splitext( file.filename)[0]+"_col"
    
    print(collection_name)

    content = await file.read()

    async with aiofiles.open(file_path, "wb") as f:
       await f.write(content)

    chunks = ingest_document(file_path,collection_name)

    return {"status": "success","collection-name":collection_name, "total-chunks": chunks}

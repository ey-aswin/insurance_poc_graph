from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.controllers.embedding_controller import (EmbeddingController,
                                                  get_embedding_controller)

router = APIRouter(prefix="/api/v1/embedding", tags=["embedding"])

@router.post("/upload/graph")
async def upload_embedding(file: UploadFile, embedding_controller: EmbeddingController = Depends(get_embedding_controller)):
    try:
        uploads = await embedding_controller.upload_embedding_graph(files=[file])
        return {"message": "Embeddings uploaded successfully!", "details": uploads}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
    

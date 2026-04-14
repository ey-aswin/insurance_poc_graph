import logging
from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.models.schemas.schema import GraphData
from app.services.embedding_service import EmbeddingService
from app.services.neo4j_service import neo4j_service
from app.services.qdrant_service import QdrantService
from app.services.tokenization_service import tokenize_service
from azure.cosmos_db import get_container
from app.services.prompt_service import PromptService

logger = logging.getLogger(__name__)

class EmbeddingController:
    def __init__(self):
        pass

    async def upload_embedding_graph(self, files:List[UploadFile]):
        try:
                # GET THE FILES 
            raw_files = files
        
            # CHUNK THE FILES
            logger.info("Starting tokenization of files")
            tokenized_docs= await tokenize_service.tokenize_files(raw_files=raw_files)
            logger.info("Tokenization completed. Number of chunks created: %s", len(tokenized_docs))
            # logger.info(tokenized_docs)
            session_id = str(uuid4())  # Generate a unique session ID for this batch of documents
           
            # GENERATE THE EMBEDDINGS
            logger.info("Starting embedding generation")
            logger.info(f"Tokenized documents: {tokenized_docs[:1]}")  # Log the first few tokenized documents for debugging
            embedding_service = EmbeddingService()
            embedding_info  = embedding_service.generate_embeddings(tokenized_docs,session_id=session_id)
            logger.info("Embedding generation completed for session ID: %s", session_id)
            
            # STORE THE EMBEDDINGS
            logger.info("Starting to store embeddings in Neo4j for session ID: %s", session_id)
            logger.info(f"Embedding info to be stored: {embedding_info}")
            neo4j_service.store_embeddings(embedding=embedding_info)
            logger.info("Successfully stored embeddings in Neo4j for session ID: %s", session_id)
            
            # Generate graph data 
            print("embedding info before graph extraction:", embedding_info[0])
            logger.info("Starting graph data extraction using LLM for session ID: %s", session_id)
            prompt_service = PromptService()
            graph_data = await prompt_service.extract_graph_info(embedding_info)
            logger.info("Graph data extraction completed for session ID: %s", session_id)
            
            
            
            # Store the graph data in Neo4j
            logger.info("Starting to store graph data in Neo4j for session ID: %s", session_id)
            neo4j_service.store_graph_data(graph=graph_data, session_id=session_id) 
            logger.info("Successfully stored graph data in Neo4j for session ID: %s", session_id)
            
           
            # Store metadata in Cosmos DB
            cosmos_db = get_container("uploads_metadata")
            logger.info("Storing embedding metadata in Cosmos DB for session ID: %s", session_id)
            cosmos_db.create_item({
                "id": session_id,  # Use session_id as the unique identifier for Cosmos DB item
                "session_id": session_id,  # Use session_id as the unique identifier for the metadata
                "file_name": raw_files[0].filename,  # Assuming single file upload for simplicity
                "num_chunks": len(tokenized_docs),
                "user_id": "admin",  # Placeholder for user ID, replace with actual user identification logic
                "creation_timestamp": datetime.utcnow().isoformat()  # Store the timestamp of when the embedding was created
            })
            logger.info("Embedding metadata stored successfully in Cosmos DB for session ID: %s", session_id)
            return {"message": "Embedding uploaded successfully!", "session_id": session_id}
    
        except Exception as e:
            logger.exception("Error uploading embedding")
            raise HTTPException(status_code=500, detail=f"Failed to upload embedding: {str(e)}")


        
    
def get_embedding_controller():
    return EmbeddingController()    
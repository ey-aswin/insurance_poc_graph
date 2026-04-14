 
import json
import logging
from uuid import uuid4

from openai import AzureOpenAI

from app.config.settings import settings
from app.models.schemas.schema import FileEmbeddingInfo
from app.services.prompt_service import PromptService

logger = logging.getLogger(__name__)

AZURE_OPENAI_ENDPOINT = settings.AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_MODEL_NAME = settings.AZURE_OPENAI_DEPLOYMENT
AZURE_OPENAI_DEPLOYMENT = settings.AZURE_OPENAI_DEPLOYMENT
AZURE_OPENAI_API_VERSION = settings.AZURE_OPENAI_API_VERSION
AZURE_OPENAI_API_KEY =settings.AZURE_OPENAI_API_KEY


class EmbeddingService():
    def __init__(self):
        self.training_client = AzureOpenAI(
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
        )
        
    def generate_embedding_for_chunk(self, text: str) -> list[float]:
        try:
            embedding_vector = self.training_client.embeddings.create(
                input=text,
                model=AZURE_OPENAI_DEPLOYMENT,
            )
            return embedding_vector.data[0].embedding if embedding_vector.data else []
        except Exception as e:
            logger.exception("Error generating embedding for chunk")
            raise Exception(f"Embedding generation for chunk failed: {str(e)}")
    
    def generate_embeddings(self, tokenized_docs, session_id: str) -> list[FileEmbeddingInfo]:
        # IMPLEMENT THE LOGIC TO GENERATE EMBEDDINGS USING OPENAI API
        try:
            embedding_info = []
            #  Create Embedding for the first chunk of the eg_chunked_docs as an example
            logger.info("Creating embedding")
            for doc in tokenized_docs:
                chunk_id = uuid4()
                embedding_vector = self.generate_embedding_for_chunk(doc.page_content)
                
                embedding_info.append(FileEmbeddingInfo(
                    chunk_id=str(chunk_id),
                    session_id=session_id,
                    embedding=embedding_vector if embedding_vector else [],
                    text=doc.page_content,
                    metadata={"source": doc.metadata.get("source", "unknown")},
                ))
            return embedding_info
    
        except Exception as e:
            logger.exception("Error generating embeddings")
            raise Exception(f"Embedding generation failed: {str(e)}")
  
        prompt_service = PromptService()
        graph_data = []
        for info in embedding_info:
            graph = prompt_service.extract_graph(info)
            graph_data.append(graph)
        return graph_data
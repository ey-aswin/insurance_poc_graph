import logging
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (Distance, FieldCondition, Filter, MatchAny,
                                  MatchValue, NamedVector, PointStruct,
                                  VectorParams)

from app.config.settings import settings
from app.models.schemas.schema import FileEmbeddingInfo

logger = logging.getLogger(__name__)

COLLECTION = "rag_docs"
EMBED_DIM = 3072
VECTOR_NAME: Optional[str] = None  # If you switch to named vectors, set a string here.


class QdrantService:
    def __init__(self):
        # Add api_key if your instance is secured
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            # api_key=settings.QDRANT_API_KEY,
        )
        logger.info("Qdrant client initialized")
        self.ensure_collection()

    def ensure_collection(self):
        """Create the collection if it doesn't exist, without dropping data."""
        try:
            self.client.get_collection(COLLECTION)
            logger.info("Qdrant collection already exists")
        except Exception:
            # Create with unnamed or named vectors depending on VECTOR_NAME
            if VECTOR_NAME:
                vectors_config = { 
                    VECTOR_NAME: VectorParams(size=EMBED_DIM, distance=Distance.COSINE) 
                }
            else:
                vectors_config = VectorParams(size=EMBED_DIM, distance=Distance.COSINE)

            self.client.create_collection(
                collection_name=COLLECTION,
                vectors_config=vectors_config,
            )
            logger.info("Qdrant collection created")

    def store_embeddings(self, embedding_info: List[FileEmbeddingInfo]):
        try:
            logger.info("Storing embeddings in Qdrant")
            points: List[PointStruct] = []
            for item in embedding_info:
                # Ensure these fields are correctly typed and present
                points.append(
                    PointStruct(
                        id=item.chunk_id,            # str or int is fine; must be unique per chunk
                        vector=item.embedding,       # length must equal EMBED_DIM
                        payload={
                            "metadata": item.metadata,  # dict is ok
                            "text": item.text,
                            "file_id": item.file_id,
                        },
                    )
                )

            logger.info(f"Prepared {len(points)} points for upsert into Qdrant")
            self.client.upsert(
                collection_name=COLLECTION,
                points=points,
                wait=True,  # optional: wait until indexed
            )
            logger.info("Embeddings stored successfully in Qdrant")

        except Exception as e:
            logger.error(f"Error storing embeddings: {e}", exc_info=True)
            raise Exception(f"Failed to store embeddings: {str(e)}")

    def qdrant_search(
        self,
        q_emb: List[float],
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ):
        # Build filter (if any)
        q_filter = None
        if filters:
            must = []
            for k, v in filters.items():
                # Use correct key path: e.g., "file_id" or "metadata.author"
                if isinstance(v, list):
                    must.append(FieldCondition(key=k, match=MatchAny(any=v)))
                else:
                    must.append(FieldCondition(key=k, match=MatchValue(value=v)))
            q_filter = Filter(must=must)

        # Named vs unnamed vector
        query = NamedVector(name=VECTOR_NAME, vector=q_emb) if VECTOR_NAME else q_emb

        res = self.client.query_points(
            collection_name=COLLECTION,
            query=query,
            query_filter=q_filter,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        )

        points = getattr(res, "points", res)
        return points  # list[ScoredPoint]
from pydantic import BaseModel


class FileEmbeddingInfo(BaseModel):
    chunk_id: str
    session_id: str
    embedding: list
    text: str
    metadata: dict

class ChunkInfo(BaseModel):
    chunk_id: str
    text: str
    metadata: dict

class GraphData(BaseModel):
    entities: list
    relationships: list
    chunks: ChunkInfo
    embedding: list
    text: str

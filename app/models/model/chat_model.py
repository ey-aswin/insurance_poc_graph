import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ChatSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    linked_claim_id: str
    status: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
class ChatMessage(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    chat_session_id:str
    sender:str
    message:str
    message_type:str
    timestamp:str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict = None
  
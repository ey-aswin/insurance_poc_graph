import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class StatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DISABLED = "DISABLED"
        
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    hashed_password: str
    status: StatusEnum = StatusEnum.ACTIVE  # default status is 'ACTIVE'
    phone_number: str = None
    role: str = "user"  # default role is 'user', can be 'admin' or 'user'  
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())  
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
class AuditLogs(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    entity_type: str
    entity_id: str
    action: str
    metadata: dict[str, Any] | None = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
class UserProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    profile_allowed_permissions: dict[str, Any] | None = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
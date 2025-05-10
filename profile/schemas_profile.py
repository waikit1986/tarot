from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel

class ProfileBase(BaseModel):
    user_name: str
    age: int
    bio: str

class ProfileCreate(ProfileBase):
    pass

class ProfileDeleteResponse(BaseModel):
    id: UUID
    message: str = "Profile deleted successfully"
    deleted_at: datetime

class ProfileUpdate(BaseModel):
    user_name: Optional[str] = None
    age: Optional[int] = None
    bio: Optional[str] = None

    class Config:
        extra = "forbid"  # Prevent unexpected fields

class ProfileResponse(ProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ProfileBase(BaseModel):
    user_name: str
    age: int
    bio: str | None = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    user_name: str | None = None
    age: int | None = None
    bio: str | None = None

class ProfileOut(ProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProfileDeleted(BaseModel):
    id: UUID

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) # fk of users.id table with cascade - apple login
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    user_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    bio = Column(String, nullable=False)

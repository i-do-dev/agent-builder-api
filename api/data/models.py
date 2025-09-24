import uuid
from sqlalchemy import Column, String, Text, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID as PG_UUID
from api.data.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)  # Hashed password stored
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Agent(Base):
    __tablename__ = "agents"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    api_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    role = Column(Text, nullable=True)
    organization = Column(Text, nullable=True)
    user_type = Column(String, nullable=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    modified_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Relationships
    user = relationship(
        "User",
        back_populates="agents",
        foreign_keys=[user_id]  # Explicitly specify the foreign key
    )
    modifier = relationship(
        "User",
        foreign_keys=[modified_by],  # Explicitly specify the foreign key
        overlaps="agents"  # Avoid overlap warnings
    )
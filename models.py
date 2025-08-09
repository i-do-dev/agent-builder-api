import uuid
from sqlalchemy import Column, String, Text, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID as PG_UUID
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)  # Hashed password stored
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    # Relationship with Agent (explicitly specify foreign_keys)
    agents = relationship(
        "Agent",
        back_populates="user",
        foreign_keys="[Agent.user_id]"  # Specify the foreign key explicitly
    )


class Agent(Base):
    __tablename__ = "agents"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    api_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    role = Column(Text, nullable=True)
    organization = Column(Text, nullable=True)
    topics = relationship(
        "Topic",
        back_populates="agent",
        cascade="all, delete-orphan"
    )  # Cascade deletes to topics
    user_type = Column(String, nullable=True)
    
    # Foreign keys
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

class Topic(Base):
    __tablename__ = "topics"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String, nullable=False)
    classification_description = Column(Text, nullable=True)
    scope = Column(Text, nullable=True)
    agent_id = Column(PG_UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    agent = relationship("Agent", back_populates="topics")
    topic_instructions = relationship(
        "TopicInstruction", back_populates="topic", cascade="all, delete-orphan"
    )  # Cascade deletes to topic_instructions

class TopicInstruction(Base):
    __tablename__ = "topic_instructions"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id = Column(PG_UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    instruction = Column(Text, nullable=False)
    topic = relationship("Topic", back_populates="topic_instructions")
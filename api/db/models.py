import uuid
from sqlalchemy import Column, String, Text, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID
from api.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)  # Hashed password stored
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship with Agent
    agents = relationship(
        "Agent",
        back_populates="user"
    )

class Agent(Base):
    __tablename__ = "agents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    api_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    role = Column(Text, nullable=True)
    organization = Column(Text, nullable=True)
    user_type = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationships
    user = relationship(
        "User",
        back_populates="agents",
        foreign_keys=[user_id]  # Explicitly specify the foreign key
    )
    topics = relationship(
        "Topic",
        back_populates="agent",
        cascade="all, delete-orphan"
    )  # Cascade deletes to topics

class Topic(Base):
    __tablename__ = "topics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String, nullable=False)
    classification_description = Column(Text, nullable=True)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    # Relationship with Agent
    agent = relationship(
        "Agent",
        back_populates="topics",
        foreign_keys=[agent_id]  # Explicitly specify the foreign key
    )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    topic_instructions = relationship(
        "TopicInstructions",
        back_populates="topic",
        cascade="all, delete-orphan"
    )  # Cascade deletes to topic instructions

class TopicInstructions(Base):
    __tablename__ = "topic_instructions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instructions = Column(Text, nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship with Topic
    topic = relationship(
        "Topic", 
        back_populates="topic_instructions",
        foreign_keys=[topic_id]
    )

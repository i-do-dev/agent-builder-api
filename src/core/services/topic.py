from api.dependencies.db import Db
from api.schemas.topic import TopicCreateRequest, TopicResponse
from api.db.models import Topic, TopicInstruction
from typing import List

class TopicCreator:
    """Handles the creation of a topic based on a request."""

    def __init__(self, db: Db, agent_id: str):
        self.db = db
        self.agent_id = agent_id

    async def on_request(self, topic_req: TopicCreateRequest) -> TopicResponse:
        topic_model = Topic(
            label=topic_req.label,
            classification_description=topic_req.classification_description,
            agent_id=self.agent_id
        )

        topic: Topic = await self.create(topic_model, instructions=topic_req.instructions)
        return TopicResponse(
            id=topic.id,
            label=topic.label,
            classification_description=topic.classification_description,
            agent_id=topic.agent_id,
            instructions=[ti.instruction for ti in topic.instructions]
        )
    
    async def create(self, topic: Topic, instructions: List[str] = []) -> Topic:
        return await self.db.topic.add(topic, instructions=instructions)
    
class TopicService:
    """Service for managing topics."""

    def __init__(self, db: Db, agent_id: str):
        self.db = db
        self.agent_id = agent_id

    async def create_on_request(self, topic_req: TopicCreateRequest) -> TopicResponse:
        topic_creator = TopicCreator(db=self.db, agent_id=self.agent_id)
        response = await topic_creator.on_request(topic_req=topic_req)
        return response
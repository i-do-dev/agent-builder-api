from src.adapters.db.uow import UnitOfWork
from src.core.entities.topic import Topic
from src.handlers.contracts.topic import TopicCreateCommand, TopicResult


class TopicCreateCommandHandler:
    def __init__(self, db: UnitOfWork, agent_id: str):
        self.db = db
        self.agent_id = agent_id

    async def create_on_request(self, command: TopicCreateCommand) -> TopicResult:
        entity = Topic(
            label=command.label,
            classification_description=command.classification_description,
            agent_id=self.agent_id,
        )
        topic = await self.db.topic.add(entity)
        return TopicResult(
            id=topic.id,
            label=topic.label,
            classification_description=topic.classification_description,
            instructions=[],
            agent=None,
        )

from typing import List, Optional

from sqlalchemy import or_
from api.db.repositories.base import Repository
from api.db.models import Topic, TopicInstruction

class TopicRepository(Repository[Topic]):
    """Repository for Topic model."""
    model = Topic

    async def add(self, obj: Topic, instructions: List[str] = []) -> Topic:
        # add topic instructions if any
        for instruction in instructions:
            obj.instructions.append(
                TopicInstruction(instruction=instruction)
            )
        return await super().add(obj)
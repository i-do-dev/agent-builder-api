from typing import Optional
from uuid import UUID
import json
from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import LessonProject as LessonProjectModel
from src.core.entities.lesson import LessonProject as LessonProjectEntity
from src.adapters.db.mappers.lesson import LessonProjectMapper


class LessonProjectRepository(Repository[LessonProjectEntity, LessonProjectModel]):
    model = LessonProjectModel

    async def _model_to_entity(self, model: LessonProjectModel) -> LessonProjectEntity:
        return LessonProjectMapper.model_to_entity(model)

    async def _entity_to_model(self, entity: LessonProjectEntity) -> LessonProjectModel:
        return LessonProjectMapper.entity_to_model(entity)

    async def get_for_instructor(self, lesson_id: UUID, instructor_user_id: UUID) -> Optional[LessonProjectEntity]:
        return await self.get_by(id=lesson_id, instructor_user_id=instructor_user_id)

    async def update_status(
        self,
        lesson_id: UUID,
        status: str,
        review_notes: str | None = None,
    ) -> Optional[LessonProjectEntity]:
        model = await self.get_model(lesson_id)
        if model is None:
            return None
        model.status = status
        model.review_notes = review_notes
        await self.session.flush([model])
        return await self._model_to_entity(model)

    async def update_generated_content(
        self,
        lesson_id: UUID,
        outline: list[dict] | None = None,
        resource_recommendations: dict[str, list[dict]] | None = None,
    ) -> Optional[LessonProjectEntity]:
        model = await self.get_model(lesson_id)
        if model is None:
            return None
        if outline is not None:
            model.outline_json = json.dumps(outline)
        if resource_recommendations is not None:
            model.resource_recommendations_json = json.dumps(resource_recommendations)
        await self.session.flush([model])
        return await self._model_to_entity(model)

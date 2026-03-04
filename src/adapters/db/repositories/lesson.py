from typing import Optional
from uuid import UUID
import json
from sqlalchemy import desc, select
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

    async def list_for_instructor(
        self,
        instructor_user_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[LessonProjectEntity], int]:
        offset = (page - 1) * page_size

        total = await self.count(instructor_user_id=instructor_user_id)

        statement = (
            select(self.model)
            .where(self.model.instructor_user_id == instructor_user_id)
            .order_by(desc(self.model.updated_at))
            .offset(offset)
            .limit(page_size)
        )
        result = await self.session.execute(statement)
        models = result.scalars().all()
        lessons = [await self._model_to_entity(model) for model in models]
        return lessons, total

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
        summary: dict | None = None,
        assessments: list[dict] | None = None,
        thematic_mapping: list[dict] | None = None,
    ) -> Optional[LessonProjectEntity]:
        model = await self.get_model(lesson_id)
        if model is None:
            return None
        if outline is not None:
            model.outline_json = json.dumps(outline)
        if resource_recommendations is not None:
            model.resource_recommendations_json = json.dumps(resource_recommendations)
        if summary is not None:
            model.summary_json = json.dumps(summary)
        if assessments is not None:
            model.assessments_json = json.dumps(assessments)
        if thematic_mapping is not None:
            model.thematic_mapping_json = json.dumps(thematic_mapping)
        await self.session.flush([model])
        return await self._model_to_entity(model)

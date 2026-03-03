import json
from src.adapters.db.models import LessonProject as LessonProjectModel
from src.core.entities.lesson import LessonProject as LessonProjectEntity


class LessonProjectMapper:
    @staticmethod
    def _loads(payload: str | None, default_value):
        if payload is None:
            return default_value
        try:
            return json.loads(payload)
        except (TypeError, ValueError):
            return default_value

    @staticmethod
    def _dumps(payload) -> str | None:
        if payload is None:
            return None
        return json.dumps(payload)

    @staticmethod
    def model_to_entity(model: LessonProjectModel) -> LessonProjectEntity:
        return LessonProjectEntity(
            id=model.id,
            topic=model.topic,
            audience=model.audience,
            instructional_focus=model.instructional_focus,
            status=model.status,
            review_notes=model.review_notes,
            instructor_user_id=model.instructor_user_id,
            outline=LessonProjectMapper._loads(model.outline_json, []),
            resource_recommendations=LessonProjectMapper._loads(model.resource_recommendations_json, {}),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def entity_to_model(entity: LessonProjectEntity) -> LessonProjectModel:
        kwargs = {
            "topic": entity.topic,
            "audience": entity.audience,
            "instructional_focus": entity.instructional_focus,
            "status": entity.status,
            "review_notes": entity.review_notes,
            "outline_json": LessonProjectMapper._dumps(entity.outline),
            "resource_recommendations_json": LessonProjectMapper._dumps(entity.resource_recommendations),
            "instructor_user_id": entity.instructor_user_id,
        }
        if entity.id is not None:
            kwargs["id"] = entity.id
        return LessonProjectModel(**kwargs)

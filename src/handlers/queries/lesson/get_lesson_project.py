from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.handlers.contracts.lesson import (
    LessonResult,
    OutlineSectionResult,
    ResourceRecommendationResult,
)
from src.handlers.errors import NotFoundError


class GetLessonProjectQueryHandler:
    def __init__(self, db: UnitOfWork):
        self.db = db

    async def get(self, lesson_id: UUID, instructor_username: str) -> LessonResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = await self.db.lesson.get_for_instructor(lesson_id, instructor.id)
        if not lesson:
            raise NotFoundError("Lesson project not found")

        outline = [
            OutlineSectionResult(title=section["title"], bullets=section["bullets"])
            for section in (lesson.outline or [])
        ]

        recommendations = {}
        for subtopic, items in (lesson.resource_recommendations or {}).items():
            recommendations[subtopic] = [
                ResourceRecommendationResult(
                    title=item["title"],
                    url=item["url"],
                    source=item["source"],
                    resource_type=item["resource_type"],
                    rationale=item["rationale"],
                )
                for item in items
            ]

        return LessonResult(
            id=lesson.id,
            topic=lesson.topic,
            audience=lesson.audience,
            instructional_focus=lesson.instructional_focus,
            status=lesson.status,
            instructor_user_id=lesson.instructor_user_id,
            review_notes=lesson.review_notes,
            created_at=lesson.created_at,
            updated_at=lesson.updated_at,
            outline=outline,
            resource_recommendations=recommendations,
        )

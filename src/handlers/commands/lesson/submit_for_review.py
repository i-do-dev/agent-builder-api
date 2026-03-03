from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.entities.lesson import LessonStatus
from src.handlers.contracts.lesson import LessonResult
from src.handlers.errors import NotFoundError, ValidationError


class LessonSubmitForReviewCommandHandler:
    def __init__(self, db: UnitOfWork):
        self.db = db

    async def submit(self, lesson_id: UUID, instructor_username: str) -> LessonResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = await self.db.lesson.get_for_instructor(lesson_id, instructor.id)
        if not lesson:
            raise NotFoundError("Lesson project not found")

        if lesson.status != LessonStatus.DRAFT:
            raise ValidationError("Only draft lessons can be submitted for review")

        updated = await self.db.lesson.update_status(lesson.id, LessonStatus.IN_REVIEW, lesson.review_notes)
        return LessonResult(
            id=updated.id,
            topic=updated.topic,
            audience=updated.audience,
            instructional_focus=updated.instructional_focus,
            status=updated.status,
            instructor_user_id=updated.instructor_user_id,
            review_notes=updated.review_notes,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )

from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.entities.lesson import LessonStatus
from src.handlers.contracts.lesson import LessonResult
from src.handlers.errors import NotFoundError, ValidationError


class LessonApprovalDecisionCommandHandler:
    def __init__(self, db: UnitOfWork):
        self.db = db

    async def apply(
        self,
        lesson_id: UUID,
        decision: str,
        instructor_username: str,
        review_notes: str | None = None,
    ) -> LessonResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = await self.db.lesson.get_for_instructor(lesson_id, instructor.id)
        if not lesson:
            raise NotFoundError("Lesson project not found")

        if lesson.status != LessonStatus.IN_REVIEW:
            raise ValidationError("Approval decisions can be applied only to in-review lessons")

        normalized = decision.lower()
        if normalized in {"reject", "edit"} and (review_notes is None or not review_notes.strip()):
            raise ValidationError("review_notes is required for reject or edit decisions")

        if normalized == "approve":
            next_status = LessonStatus.APPROVED
        elif normalized == "reject":
            next_status = LessonStatus.REJECTED
        elif normalized == "edit":
            next_status = LessonStatus.NEEDS_REVISION
        else:
            raise ValidationError("Invalid decision. Allowed: approve, reject, edit")

        updated = await self.db.lesson.update_status(lesson.id, next_status, review_notes)
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

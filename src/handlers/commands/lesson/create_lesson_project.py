from src.adapters.db.uow import UnitOfWork
from src.core.entities.lesson import LessonProject
from src.handlers.contracts.lesson import LessonCreateCommand, LessonResult
from src.handlers.errors import NotFoundError


class LessonCreateCommandHandler:
    def __init__(self, db: UnitOfWork):
        self.db = db

    async def create_on_request(self, command: LessonCreateCommand, instructor_username: str) -> LessonResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = LessonProject(
            topic=command.topic,
            audience=command.audience,
            instructional_focus=command.instructional_focus,
            instructor_user_id=instructor.id,
        )
        created = await self.db.lesson.add(lesson)
        return LessonResult(
            id=created.id,
            topic=created.topic,
            audience=created.audience,
            instructional_focus=created.instructional_focus,
            status=created.status,
            instructor_user_id=created.instructor_user_id,
            review_notes=created.review_notes,
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

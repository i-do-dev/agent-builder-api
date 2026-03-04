from src.adapters.db.uow import UnitOfWork
from src.core.entities.lesson import LessonProject
from src.handlers.contracts.lesson import LessonCreateCommand, LessonResult
from src.handlers.errors import NotFoundError


class LessonCreateCommandHandler:
    def __init__(self, db: UnitOfWork):
        self.db = db

    async def create_on_request(self, lesson_command: LessonCreateCommand, instructor_username: str) -> LessonResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = LessonProject(
            topic=lesson_command.topic,
            audience=lesson_command.audience,
            instructional_focus=lesson_command.instructional_focus,
            instructor_user_id=instructor.id,
        )
        lesson_created = await self.db.lesson.add(lesson)
        return LessonResult(
            id=lesson_created.id,
            topic=lesson_created.topic,
            audience=lesson_created.audience,
            instructional_focus=lesson_created.instructional_focus,
            status=lesson_created.status,
            instructor_user_id=lesson_created.instructor_user_id,
            review_notes=lesson_created.review_notes,
            created_at=lesson_created.created_at,
            updated_at=lesson_created.updated_at,
        )

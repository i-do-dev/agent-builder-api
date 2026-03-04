from src.adapters.db.uow import UnitOfWork
from src.handlers.contracts.lesson import LessonListResult, LessonResult
from src.handlers.errors import NotFoundError


class ListLessonsQueryHandler:
    def __init__(self, db: UnitOfWork):
        self.db = db

    async def list(
        self,
        instructor_username: str,
        page: int = 1,
        page_size: int = 10,
    ) -> LessonListResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lessons, total = await self.db.lesson.list_for_instructor(
            instructor_user_id=instructor.id,
            page=page,
            page_size=page_size,
        )

        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return LessonListResult(
            lessons=[
                LessonResult(
                    id=lesson.id,
                    topic=lesson.topic,
                    audience=lesson.audience,
                    instructional_focus=lesson.instructional_focus,
                    status=lesson.status,
                    instructor_user_id=lesson.instructor_user_id,
                    review_notes=lesson.review_notes,
                    created_at=lesson.created_at,
                    updated_at=lesson.updated_at,
                )
                for lesson in lessons
            ],
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )
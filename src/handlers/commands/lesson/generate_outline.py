from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.services.lesson_planner import LessonPlannerService
from src.handlers.contracts.lesson import LessonOutlineResult, OutlineSectionResult
from src.handlers.errors import NotFoundError


class LessonGenerateOutlineCommandHandler:
    def __init__(self, db: UnitOfWork, planner: LessonPlannerService | None = None):
        self.db = db
        self.planner = planner or LessonPlannerService()

    async def generate(self, lesson_id: UUID, instructor_username: str) -> LessonOutlineResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = await self.db.lesson.get_for_instructor(lesson_id, instructor.id)
        if not lesson:
            raise NotFoundError("Lesson project not found")

        generated_outline = self.planner.generate_outline(
            topic=lesson.topic,
            audience=lesson.audience,
            instructional_focus=lesson.instructional_focus,
        )

        updated = await self.db.lesson.update_generated_content(lesson_id=lesson.id, outline=generated_outline)
        return LessonOutlineResult(
            lesson_id=updated.id,
            outline=[
                OutlineSectionResult(title=section["title"], bullets=section["bullets"])
                for section in (updated.outline or [])
            ],
        )

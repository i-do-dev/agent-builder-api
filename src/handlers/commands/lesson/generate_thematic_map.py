from src.adapters.db.uow import UnitOfWork
from src.core.services.lesson_planner import LessonPlannerService
from src.handlers.contracts.lesson import LessonThematicMapResult, ThematicMappingItemResult
from src.handlers.errors import NotFoundError


class LessonGenerateThematicMapCommandHandler:
    def __init__(self, db: UnitOfWork, planner: LessonPlannerService | None = None):
        self.db = db
        self.planner = planner or LessonPlannerService()

    async def generate(
        self,
        lesson_id,
        instructor_username: str,
        cross_disciplinary_focus: str,
    ) -> LessonThematicMapResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = await self.db.lesson.get_for_instructor(lesson_id, instructor.id)
        if not lesson:
            raise NotFoundError("Lesson project not found")

        mapping = self.planner.generate_thematic_mapping(
            topic=lesson.topic,
            instructional_focus=lesson.instructional_focus,
            cross_disciplinary_focus=cross_disciplinary_focus,
        )

        updated = await self.db.lesson.update_generated_content(lesson_id=lesson.id, thematic_mapping=mapping)
        return LessonThematicMapResult(
            lesson_id=updated.id,
            cross_disciplinary_focus=cross_disciplinary_focus,
            mapping=[
                ThematicMappingItemResult(
                    concept=item["concept"],
                    societal_impact=item["societal_impact"],
                    explanation=item["explanation"],
                )
                for item in (updated.thematic_mapping or [])
            ],
        )

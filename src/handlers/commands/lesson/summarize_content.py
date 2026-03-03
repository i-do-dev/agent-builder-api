from src.adapters.db.uow import UnitOfWork
from src.core.services.lesson_planner import LessonPlannerService
from src.handlers.contracts.lesson import LessonSummaryResult, SummaryResult
from src.handlers.errors import NotFoundError, ValidationError


class LessonSummarizeContentCommandHandler:
    def __init__(self, db: UnitOfWork, planner: LessonPlannerService | None = None):
        self.db = db
        self.planner = planner or LessonPlannerService()

    async def summarize(
        self,
        lesson_id,
        instructor_username: str,
        source_text: str | None = None,
        source_url: str | None = None,
    ) -> LessonSummaryResult:
        if not source_text and not source_url:
            raise ValidationError("Either source_text or source_url is required")

        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = await self.db.lesson.get_for_instructor(lesson_id, instructor.id)
        if not lesson:
            raise NotFoundError("Lesson project not found")

        summary_payload = self.planner.summarize_content(
            topic=lesson.topic,
            instructional_focus=lesson.instructional_focus,
            source_text=source_text,
            source_url=source_url,
        )

        updated = await self.db.lesson.update_generated_content(lesson_id=lesson.id, summary=summary_payload)
        summary = updated.summary or {}
        return LessonSummaryResult(
            lesson_id=updated.id,
            summary=SummaryResult(
                source_url=summary.get("source_url"),
                key_points=summary.get("key_points", []),
                extracted_parameters=summary.get("extracted_parameters", []),
                concise_summary=summary.get("concise_summary", ""),
            ),
        )

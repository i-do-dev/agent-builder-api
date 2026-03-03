from src.adapters.db.uow import UnitOfWork
from src.core.services.lesson_planner import LessonPlannerService
from src.handlers.contracts.lesson import AssessmentQuestionResult, LessonAssessmentResult
from src.handlers.errors import NotFoundError


class LessonGenerateAssessmentCommandHandler:
    def __init__(self, db: UnitOfWork, planner: LessonPlannerService | None = None):
        self.db = db
        self.planner = planner or LessonPlannerService()

    async def generate(
        self,
        lesson_id,
        instructor_username: str,
        question_count: int = 10,
    ) -> LessonAssessmentResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = await self.db.lesson.get_for_instructor(lesson_id, instructor.id)
        if not lesson:
            raise NotFoundError("Lesson project not found")

        assessments = self.planner.generate_assessment(
            topic=lesson.topic,
            audience=lesson.audience,
            instructional_focus=lesson.instructional_focus,
            summary=lesson.summary,
            question_count=question_count,
        )

        updated = await self.db.lesson.update_generated_content(lesson_id=lesson.id, assessments=assessments)
        return LessonAssessmentResult(
            lesson_id=updated.id,
            questions=[
                AssessmentQuestionResult(
                    question=item["question"],
                    options=item["options"],
                    answer=item["answer"],
                    rationale=item["rationale"],
                )
                for item in (updated.assessments or [])
            ],
        )

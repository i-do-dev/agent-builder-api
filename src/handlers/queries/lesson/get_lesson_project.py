from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.handlers.contracts.lesson import (
    AssessmentQuestionResult,
    LessonResult,
    OutlineSectionResult,
    ResourceRecommendationResult,
    SummaryResult,
    ThematicMappingItemResult,
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

        lesson_summary = getattr(lesson, "summary", None)
        lesson_assessments = getattr(lesson, "assessments", None)

        summary = None
        if lesson_summary:
            summary = SummaryResult(
                source_url=lesson_summary.get("source_url"),
                key_points=lesson_summary.get("key_points", []),
                extracted_parameters=lesson_summary.get("extracted_parameters", []),
                concise_summary=lesson_summary.get("concise_summary", ""),
            )

        assessments = [
            AssessmentQuestionResult(
                question=item["question"],
                options=item["options"],
                answer=item["answer"],
                rationale=item["rationale"],
            )
            for item in (lesson_assessments or [])
        ]

        thematic_mapping = [
            ThematicMappingItemResult(
                concept=item["concept"],
                societal_impact=item["societal_impact"],
                explanation=item["explanation"],
            )
            for item in (getattr(lesson, "thematic_mapping", None) or [])
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
            summary=summary,
            assessments=assessments,
            thematic_mapping=thematic_mapping,
        )

from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.services.lesson_planner import LessonPlannerService
from src.handlers.contracts.lesson import LessonSubtopicResourcesResult, ResourceRecommendationResult
from src.handlers.errors import NotFoundError


class LessonExpandSubtopicResourcesCommandHandler:
    def __init__(self, db: UnitOfWork, planner: LessonPlannerService | None = None):
        self.db = db
        self.planner = planner or LessonPlannerService()

    async def expand(self, lesson_id: UUID, subtopic: str, instructor_username: str) -> LessonSubtopicResourcesResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = await self.db.lesson.get_for_instructor(lesson_id, instructor.id)
        if not lesson:
            raise NotFoundError("Lesson project not found")

        generated_resources = self.planner.recommend_resources(subtopic=subtopic, audience=lesson.audience)

        current = lesson.resource_recommendations or {}
        current[subtopic] = generated_resources

        updated = await self.db.lesson.update_generated_content(
            lesson_id=lesson.id,
            resource_recommendations=current,
        )

        resources = (updated.resource_recommendations or {}).get(subtopic, [])
        return LessonSubtopicResourcesResult(
            lesson_id=updated.id,
            subtopic=subtopic,
            resources=[
                ResourceRecommendationResult(
                    title=item["title"],
                    url=item["url"],
                    source=item["source"],
                    resource_type=item["resource_type"],
                    rationale=item["rationale"],
                )
                for item in resources
            ],
        )

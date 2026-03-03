from uuid import UUID
from src.adapters.deepagents.lesson_runtime import DeepLessonAgentRuntime
from src.adapters.db.uow import UnitOfWork
from src.core.services.lesson_planner import LessonPlannerService
from src.handlers.contracts.lesson import DeepAgentRunCommand, DeepAgentRunResult
from src.handlers.errors import NotFoundError


class LessonRunDeepAgentCommandHandler:
    def __init__(
        self,
        db: UnitOfWork,
        planner: LessonPlannerService | None = None,
        deep_agent_runtime: DeepLessonAgentRuntime | None = None,
    ):
        self.db = db
        self.planner = planner or LessonPlannerService()
        self.deep_agent_runtime = deep_agent_runtime or DeepLessonAgentRuntime(planner=self.planner)

    @staticmethod
    def _classify_intent(prompt: str) -> str:
        lowered = prompt.lower()
        if any(token in lowered for token in ["outline", "discover", "structure", "plan"]):
            return "outline"
        if any(token in lowered for token in ["resource", "sources", "deep-dive", "subtopic"]):
            return "resources"
        if any(token in lowered for token in ["summarize", "summary", "synthesis"]):
            return "summary"
        if any(token in lowered for token in ["assessment", "quiz", "mcq", "question"]):
            return "assessment"
        if any(token in lowered for token in ["theme", "cross-disciplinary", "societal", "impact"]):
            return "themes"
        return "full_pipeline"

    async def run(
        self,
        lesson_id: UUID,
        instructor_username: str,
        command: DeepAgentRunCommand,
    ) -> DeepAgentRunResult:
        instructor = await self.db.user.get_by_username(instructor_username)
        if not instructor:
            raise NotFoundError("Instructor not found")

        lesson = await self.db.lesson.get_for_instructor(lesson_id, instructor.id)
        if not lesson:
            raise NotFoundError("Lesson project not found")

        intent = self._classify_intent(command.prompt)
        runtime_result = await self.deep_agent_runtime.execute(lesson=lesson, command=command, intent=intent)

        if not command.execute:
            return DeepAgentRunResult(
                lesson_id=lesson.id,
                intent=intent,
                todos=runtime_result.todos,
                executed=False,
                actions_taken=[],
            )

        outline_sections = 0
        resource_count = 0
        summary_generated = False
        assessment_count = 0
        thematic_mapping_count = 0

        if runtime_result.outline is not None:
            updated = await self.db.lesson.update_generated_content(lesson.id, outline=runtime_result.outline)
            outline_sections = len(updated.outline or [])
            lesson = updated

        if runtime_result.resource_recommendations is not None:
            updated = await self.db.lesson.update_generated_content(
                lesson.id,
                resource_recommendations=runtime_result.resource_recommendations,
            )
            resource_count = sum(len(resources) for resources in (updated.resource_recommendations or {}).values())
            lesson = updated

        if runtime_result.summary is not None:
            updated = await self.db.lesson.update_generated_content(lesson.id, summary=runtime_result.summary)
            summary_generated = bool(updated.summary)
            lesson = updated

        if runtime_result.assessments is not None:
            updated = await self.db.lesson.update_generated_content(lesson.id, assessments=runtime_result.assessments)
            assessment_count = len(updated.assessments or [])
            lesson = updated

        if runtime_result.thematic_mapping is not None:
            updated = await self.db.lesson.update_generated_content(
                lesson.id,
                thematic_mapping=runtime_result.thematic_mapping,
            )
            thematic_mapping_count = len(updated.thematic_mapping or [])

        return DeepAgentRunResult(
            lesson_id=lesson.id,
            intent=intent,
            todos=runtime_result.todos,
            executed=True,
            actions_taken=runtime_result.actions_taken,
            outline_sections=outline_sections,
            resource_count=resource_count,
            summary_generated=summary_generated,
            assessment_count=assessment_count,
            thematic_mapping_count=thematic_mapping_count,
        )

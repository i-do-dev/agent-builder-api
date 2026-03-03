from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.services.lesson_planner import LessonPlannerService
from src.handlers.contracts.lesson import DeepAgentRunCommand, DeepAgentRunResult
from src.handlers.errors import NotFoundError


class LessonRunDeepAgentCommandHandler:
    def __init__(self, db: UnitOfWork, planner: LessonPlannerService | None = None):
        self.db = db
        self.planner = planner or LessonPlannerService()

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

    @staticmethod
    def _todos_for_intent(intent: str) -> list[str]:
        if intent == "outline":
            return ["Generate lesson outline"]
        if intent == "resources":
            return ["Expand subtopic with curated resources"]
        if intent == "summary":
            return ["Synthesize source content summary"]
        if intent == "assessment":
            return ["Generate formative assessment questions"]
        if intent == "themes":
            return ["Generate cross-disciplinary thematic mapping"]
        return [
            "Generate lesson outline",
            "Expand subtopic resources",
            "Synthesize content summary",
            "Generate assessment",
            "Generate thematic mapping",
        ]

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
        todos = self._todos_for_intent(intent)

        if not command.execute:
            return DeepAgentRunResult(
                lesson_id=lesson.id,
                intent=intent,
                todos=todos,
                executed=False,
                actions_taken=[],
            )

        actions_taken: list[str] = []
        outline_sections = 0
        resource_count = 0
        summary_generated = False
        assessment_count = 0
        thematic_mapping_count = 0

        subtopic = command.subtopic or lesson.instructional_focus or lesson.topic
        cross_focus = command.cross_disciplinary_focus or "intellectual freedom and human rights"

        if intent in {"outline", "full_pipeline"}:
            outline = self.planner.generate_outline(lesson.topic, lesson.audience, lesson.instructional_focus)
            updated = await self.db.lesson.update_generated_content(lesson.id, outline=outline)
            outline_sections = len(updated.outline or [])
            actions_taken.append("Generated outline")
            lesson = updated

        if intent in {"resources", "full_pipeline"}:
            resources = self.planner.recommend_resources(subtopic=subtopic, audience=lesson.audience)
            merged = lesson.resource_recommendations or {}
            merged[subtopic] = resources
            updated = await self.db.lesson.update_generated_content(lesson.id, resource_recommendations=merged)
            resource_count = len((updated.resource_recommendations or {}).get(subtopic, []))
            actions_taken.append(f"Expanded resources for subtopic '{subtopic}'")
            lesson = updated

        if intent in {"summary", "full_pipeline"}:
            summary = self.planner.summarize_content(
                topic=lesson.topic,
                instructional_focus=lesson.instructional_focus,
                source_text=command.source_text,
                source_url=command.source_url,
            )
            updated = await self.db.lesson.update_generated_content(lesson.id, summary=summary)
            summary_generated = bool(updated.summary)
            actions_taken.append("Generated content summary")
            lesson = updated

        if intent in {"assessment", "full_pipeline"}:
            assessments = self.planner.generate_assessment(
                topic=lesson.topic,
                audience=lesson.audience,
                instructional_focus=lesson.instructional_focus,
                summary=lesson.summary,
                question_count=command.question_count,
            )
            updated = await self.db.lesson.update_generated_content(lesson.id, assessments=assessments)
            assessment_count = len(updated.assessments or [])
            actions_taken.append(f"Generated {assessment_count} assessment questions")
            lesson = updated

        if intent in {"themes", "full_pipeline"}:
            mapping = self.planner.generate_thematic_mapping(
                topic=lesson.topic,
                instructional_focus=lesson.instructional_focus,
                cross_disciplinary_focus=cross_focus,
            )
            updated = await self.db.lesson.update_generated_content(lesson.id, thematic_mapping=mapping)
            thematic_mapping_count = len(updated.thematic_mapping or [])
            actions_taken.append("Generated thematic mapping")

        return DeepAgentRunResult(
            lesson_id=lesson.id,
            intent=intent,
            todos=todos,
            executed=True,
            actions_taken=actions_taken,
            outline_sections=outline_sections,
            resource_count=resource_count,
            summary_generated=summary_generated,
            assessment_count=assessment_count,
            thematic_mapping_count=thematic_mapping_count,
        )

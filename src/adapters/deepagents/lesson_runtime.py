from dataclasses import dataclass
from typing import Any
from src.core.entities.lesson import LessonProject

from deepagents import SubAgent, create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend
from langchain_core.tools import tool

from src.core.services.lesson_planner import LessonPlannerService
from src.handlers.contracts.lesson import DeepAgentRunCommand


DEEP_AGENT_MODEL = "anthropic:claude-sonnet-4-5-20250929"


@dataclass(frozen=True)
class DeepLessonAgentRuntimeResult:
    todos: list[str]
    actions_taken: list[str]
    outline: list[dict] | None = None
    resource_recommendations: dict[str, list[dict]] | None = None
    summary: dict | None = None
    assessments: list[dict] | None = None
    thematic_mapping: list[dict] | None = None


class DeepLessonAgentRuntime:
    def __init__(self, planner: LessonPlannerService | None = None, model: str = DEEP_AGENT_MODEL):
        self.planner = planner or LessonPlannerService()
        self.model = model

    @staticmethod
    def _extract_last_text(agent_result: dict[str, Any]) -> str:
        messages = agent_result.get("messages") or []
        if not messages:
            return ""

        last_message = messages[-1]
        content = getattr(last_message, "content", None)
        if content is None and isinstance(last_message, dict):
            content = last_message.get("content")

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    text_value = item.get("text")
                    if text_value:
                        parts.append(str(text_value))
            return "\n".join(parts).strip()

        return str(content or "").strip()

    @staticmethod
    def _extract_todos(agent_result: dict[str, Any], fallback_text: str) -> list[str]:
        todo_entries = agent_result.get("todos") or []
        extracted: list[str] = []

        for todo in todo_entries:
            if isinstance(todo, dict):
                title = todo.get("title") or todo.get("task") or todo.get("description")
                if title:
                    extracted.append(str(title).strip())
            else:
                title = getattr(todo, "title", None) or getattr(todo, "task", None)
                if title:
                    extracted.append(str(title).strip())

        if extracted:
            return [item for item in extracted if item]

        lines = [line.strip(" -*\t") for line in fallback_text.splitlines()]
        bullet_like = [line for line in lines if line and (line[0].isalnum() or len(line) > 4)]
        return bullet_like[:8]

    async def _plan_only(
        self,
        *,
        lesson_topic: str,
        lesson_audience: str,
        lesson_instructional_focus: str,
        prompt: str,
    ) -> list[str]:
        planning_agent = create_deep_agent(
            model=self.model,
            tools=[],
            skills=[
                "Create concise ordered TODO plans",
                "Tailor tasks to lesson planning workflows",
            ],
            checkpointer=True,
            backend=lambda runtime: CompositeBackend(default=StateBackend(runtime), routes={}),
            system_prompt=(
                "You are a lesson-planning supervisor. Produce only a concise TODO plan as bullet points. "
                "Do not call tools or execute content generation."
            ),
            name="lesson_deep_agent_planner",
        )

        result = await planning_agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            f"Lesson Topic: {lesson_topic}\n"
                            f"Audience: {lesson_audience}\n"
                            f"Instructional Focus: {lesson_instructional_focus}\n"
                            f"Instructor Request: {prompt}\n"
                            "Return TODO items only."
                        ),
                    }
                ]
            }
        )
        response_text = self._extract_last_text(result)
        todos = self._extract_todos(result, response_text)
        return todos or ["Review instructor request and prepare next lesson-planning step"]

    async def execute(
        self,
        *,
        lesson: LessonProject,
        command: DeepAgentRunCommand,
        intent: str,
    ) -> DeepLessonAgentRuntimeResult:
        subtopic_default = command.subtopic or lesson.instructional_focus or lesson.topic
        cross_focus_default = command.cross_disciplinary_focus or "intellectual freedom and human rights"

        if not command.execute:
            planned_todos = await self._plan_only(
                lesson_topic=lesson.topic,
                lesson_audience=lesson.audience,
                lesson_instructional_focus=lesson.instructional_focus,
                prompt=command.prompt,
            )
            return DeepLessonAgentRuntimeResult(todos=planned_todos, actions_taken=[])

        generated: dict[str, Any] = {
            "outline": None,
            "resource_recommendations": None,
            "summary": None,
            "assessments": None,
            "thematic_mapping": None,
            "actions_taken": [],
        }

        @tool("generate_outline")
        def generate_outline() -> str:
            outline = self.planner.generate_outline(
                topic=lesson.topic,
                audience=lesson.audience,
                instructional_focus=lesson.instructional_focus,
            )
            generated["outline"] = outline
            generated["actions_taken"].append("Generated outline")
            return f"Generated outline with {len(outline)} sections"

        @tool("expand_subtopic_resources")
        def expand_subtopic_resources(subtopic: str = subtopic_default) -> str:
            resources = self.planner.recommend_resources(subtopic=subtopic, audience=lesson.audience)
            merged = dict(lesson.resource_recommendations or {})
            merged[subtopic] = resources
            generated["resource_recommendations"] = merged
            generated["actions_taken"].append(f"Expanded resources for subtopic '{subtopic}'")
            return f"Expanded resources for {subtopic} with {len(resources)} recommendations"

        @tool("summarize_content")
        def summarize_content(
            source_text: str | None = command.source_text,
            source_url: str | None = command.source_url,
        ) -> str:
            summary = self.planner.summarize_content(
                topic=lesson.topic,
                instructional_focus=lesson.instructional_focus,
                source_text=source_text,
                source_url=source_url,
            )
            generated["summary"] = summary
            generated["actions_taken"].append("Generated content summary")
            return "Generated content summary"

        @tool("generate_assessment")
        def generate_assessment(question_count: int = command.question_count) -> str:
            summary = generated.get("summary") or lesson.summary
            assessments = self.planner.generate_assessment(
                topic=lesson.topic,
                audience=lesson.audience,
                instructional_focus=lesson.instructional_focus,
                summary=summary,
                question_count=question_count,
            )
            generated["assessments"] = assessments
            generated["actions_taken"].append(f"Generated {len(assessments)} assessment questions")
            return f"Generated {len(assessments)} assessment questions"

        @tool("generate_thematic_mapping")
        def generate_thematic_mapping(cross_disciplinary_focus: str = cross_focus_default) -> str:
            mapping = self.planner.generate_thematic_mapping(
                topic=lesson.topic,
                instructional_focus=lesson.instructional_focus,
                cross_disciplinary_focus=cross_disciplinary_focus,
            )
            generated["thematic_mapping"] = mapping
            generated["actions_taken"].append("Generated thematic mapping")
            return f"Generated thematic mapping with {len(mapping)} concepts"

        tools = [
            generate_outline,
            expand_subtopic_resources,
            summarize_content,
            generate_assessment,
            generate_thematic_mapping,
        ]

        subagents = [
            SubAgent(
                name="outline_specialist",
                description="Creates lesson outlines for topic, audience, and instructional focus.",
                system_prompt="Use generate_outline when an outline is requested.",
                tools=[generate_outline],
            ),
            SubAgent(
                name="resource_specialist",
                description="Expands subtopic resources with curated references.",
                system_prompt="Use expand_subtopic_resources when resources are requested.",
                tools=[expand_subtopic_resources],
            ),
            SubAgent(
                name="summary_specialist",
                description="Synthesizes source material into concise lesson summary content.",
                system_prompt="Use summarize_content for summary or synthesis requests.",
                tools=[summarize_content],
            ),
            SubAgent(
                name="assessment_specialist",
                description="Builds formative assessments with rationales.",
                system_prompt="Use generate_assessment for quiz/question generation tasks.",
                tools=[generate_assessment],
            ),
            SubAgent(
                name="thematic_specialist",
                description="Creates cross-disciplinary thematic mappings.",
                system_prompt="Use generate_thematic_mapping for societal impact mapping.",
                tools=[generate_thematic_mapping],
            ),
        ]

        execution_agent = create_deep_agent(
            model=self.model,
            tools=[],
            subagents=subagents,
            skills=[
                "Classify instructor request intent for lesson planning",
                "Delegate to the correct specialist for the requested intent",
                "Prefer minimal, deterministic action set",
            ],
            checkpointer=True,
            backend=lambda runtime: CompositeBackend(default=StateBackend(runtime), routes={}),
            interrupt_on={},
            system_prompt=(
                "You are the lesson deep-agent supervisor. Do not execute tools directly. "
                "Delegate to the best specialist subagent and use only the minimum required specialist actions "
                "to satisfy the instructor request."
            ),
            name="lesson_deep_agent_executor",
        )

        result = await execution_agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            f"Intent: {intent}\n"
                            f"Lesson Topic: {lesson.topic}\n"
                            f"Audience: {lesson.audience}\n"
                            f"Instructional Focus: {lesson.instructional_focus}\n"
                            f"Prompt: {command.prompt}\n"
                            f"Default Subtopic: {subtopic_default}\n"
                            f"Question Count: {command.question_count}\n"
                            f"Cross-Disciplinary Focus: {cross_focus_default}\n"
                            "Delegate execution to specialist subagents only."
                        ),
                    }
                ]
            }
        )

        response_text = self._extract_last_text(result)
        todos = self._extract_todos(result, response_text)

        return DeepLessonAgentRuntimeResult(
            todos=todos,
            actions_taken=list(generated["actions_taken"]),
            outline=generated["outline"],
            resource_recommendations=generated["resource_recommendations"],
            summary=generated["summary"],
            assessments=generated["assessments"],
            thematic_mapping=generated["thematic_mapping"],
        )
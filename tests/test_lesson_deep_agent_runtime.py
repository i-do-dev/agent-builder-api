from uuid import uuid4

import pytest

from src.adapters.deepagents import lesson_runtime as runtime_module
from src.adapters.deepagents.lesson_runtime import DeepLessonAgentRuntime
from src.core.entities.lesson import LessonProject
from src.handlers.contracts.lesson import DeepAgentRunCommand


class _FakeAgent:
    def __init__(self, invoke_fn):
        self._invoke_fn = invoke_fn

    async def ainvoke(self, payload):
        return await self._invoke_fn(payload)


class _FakePlanner:
    @staticmethod
    def generate_outline(topic: str, audience: str, instructional_focus: str):
        return [{"title": f"{topic} for {audience}", "bullets": [instructional_focus]}]

    @staticmethod
    def recommend_resources(subtopic: str, audience: str):
        return [{"title": f"{subtopic}-{audience}", "url": "https://example.com"}]

    @staticmethod
    def summarize_content(topic: str, instructional_focus: str, source_text=None, source_url=None):
        return {
            "source_url": source_url,
            "key_points": [topic, instructional_focus],
            "concise_summary": "summary",
        }

    @staticmethod
    def generate_assessment(topic: str, audience: str, instructional_focus: str, summary=None, question_count: int = 10):
        return [
            {
                "question": f"What is {topic}?",
                "options": ["a", "b", "c", "d"],
                "answer": "a",
                "rationale": instructional_focus,
            }
            for _ in range(question_count)
        ]

    @staticmethod
    def generate_thematic_mapping(topic: str, instructional_focus: str, cross_disciplinary_focus: str):
        return [{"concept": topic, "societal_impact": cross_disciplinary_focus, "explanation": instructional_focus}]


def _fake_tool(name: str):
    def _decorator(func):
        func._tool_name = name
        return func

    return _decorator


@pytest.mark.asyncio
async def test_plan_only_returns_todos_without_execution(monkeypatch):
    captured = {}

    def _fake_create_deep_agent(*, name, tools, **kwargs):
        captured[name] = {"tools": tools, "kwargs": kwargs}

        async def _invoke(_payload):
            return {
                "messages": [{"content": "- Review prompt\n- Create outline\n- Prepare activities"}],
                "todos": [{"title": "Review prompt"}, {"title": "Create outline"}],
            }

        return _FakeAgent(_invoke)

    monkeypatch.setattr(runtime_module, "create_deep_agent", _fake_create_deep_agent)

    runtime = DeepLessonAgentRuntime(planner=_FakePlanner(), model="test-model")
    lesson = LessonProject(
        id=uuid4(),
        topic="Scientific Revolution",
        audience="high school",
        instructional_focus="major inventions",
    )

    result = await runtime.execute(
        lesson=lesson,
        command=DeepAgentRunCommand(prompt="Build a plan", execute=False),
        intent="outline",
    )

    assert result.actions_taken == []
    assert result.todos == ["Review prompt", "Create outline"]
    assert captured["lesson_deep_agent_planner"]["tools"] == []


@pytest.mark.asyncio
async def test_execute_delegates_via_subagents_with_no_supervisor_tools(monkeypatch):
    captured = {}

    def _fake_create_deep_agent(*, name, tools, subagents=None, **kwargs):
        captured[name] = {"tools": tools, "subagents": subagents or [], "kwargs": kwargs}

        async def _invoke(payload):
            if name == "lesson_deep_agent_executor":
                content = payload["messages"][0]["content"]
                if "Intent: full_pipeline" in content:
                    for subagent in subagents or []:
                        subagent_tools = subagent.get("tools", []) if isinstance(subagent, dict) else getattr(subagent, "tools", [])
                        for tool_fn in subagent_tools:
                            tool_fn()
                    return {
                        "messages": [{"content": "Delegated full pipeline"}],
                        "todos": [{"title": "Run full pipeline"}],
                    }

            return {"messages": [{"content": "ok"}], "todos": [{"title": "No-op"}]}

        return _FakeAgent(_invoke)

    monkeypatch.setattr(runtime_module, "create_deep_agent", _fake_create_deep_agent)
    monkeypatch.setattr(runtime_module, "tool", _fake_tool)

    runtime = DeepLessonAgentRuntime(planner=_FakePlanner(), model="test-model")
    lesson = LessonProject(
        id=uuid4(),
        topic="Scientific Revolution",
        audience="high school",
        instructional_focus="major inventions",
    )

    result = await runtime.execute(
        lesson=lesson,
        command=DeepAgentRunCommand(
            prompt="Do the full pipeline",
            execute=True,
            source_text="some source",
            question_count=3,
            subtopic="telescope",
            cross_disciplinary_focus="human rights",
        ),
        intent="full_pipeline",
    )

    assert captured["lesson_deep_agent_executor"]["tools"] == []
    assert len(captured["lesson_deep_agent_executor"]["subagents"]) == 5

    assert result.todos == ["Run full pipeline"]
    assert result.outline is not None and len(result.outline) == 1
    assert result.resource_recommendations is not None and "telescope" in result.resource_recommendations
    assert result.summary is not None
    assert result.assessments is not None and len(result.assessments) == 3
    assert result.thematic_mapping is not None and len(result.thematic_mapping) == 1
    assert len(result.actions_taken) == 5

from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import AsyncMock
import pytest

from src.handlers.commands.lesson.run_deep_agent import LessonRunDeepAgentCommandHandler
from src.handlers.contracts.lesson import DeepAgentRunCommand


@pytest.mark.asyncio
async def test_deep_agent_plan_only():
    instructor_id = uuid4()
    lesson_id = uuid4()

    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        get_for_instructor=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                topic="Scientific Revolution",
                audience="high school",
                instructional_focus="major inventions",
            )
        )
    )

    handler = LessonRunDeepAgentCommandHandler(db)
    result = await handler.run(
        lesson_id=lesson_id,
        instructor_username="teacher1",
        command=DeepAgentRunCommand(prompt="Please build a full plan", execute=False),
    )

    assert result.executed is False
    assert len(result.todos) >= 1


@pytest.mark.asyncio
async def test_deep_agent_execute_outline_intent():
    instructor_id = uuid4()
    lesson_id = uuid4()

    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        get_for_instructor=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                topic="Scientific Revolution",
                audience="high school",
                instructional_focus="major inventions",
                resource_recommendations={},
                summary=None,
            )
        ),
        update_generated_content=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                topic="Scientific Revolution",
                audience="high school",
                instructional_focus="major inventions",
                outline=[{"title": "Context", "bullets": ["b1"]}],
                resource_recommendations={},
                summary=None,
            )
        ),
    )

    handler = LessonRunDeepAgentCommandHandler(db)
    result = await handler.run(
        lesson_id=lesson_id,
        instructor_username="teacher1",
        command=DeepAgentRunCommand(prompt="Generate outline for this lesson", execute=True),
    )

    assert result.executed is True
    assert result.intent == "outline"
    assert result.outline_sections == 1

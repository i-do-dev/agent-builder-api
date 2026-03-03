from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import AsyncMock
import pytest

from src.handlers.commands.lesson.expand_subtopic_resources import LessonExpandSubtopicResourcesCommandHandler
from src.handlers.commands.lesson.generate_outline import LessonGenerateOutlineCommandHandler
from src.handlers.queries.lesson.get_lesson_project import GetLessonProjectQueryHandler


@pytest.mark.asyncio
async def test_generate_outline_persists_and_returns_sections():
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
        ),
        update_generated_content=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                outline=[
                    {"title": "Context & Objectives", "bullets": ["b1", "b2"]},
                    {"title": "Core Concepts", "bullets": ["b3"]},
                ],
            )
        ),
    )

    handler = LessonGenerateOutlineCommandHandler(db)
    result = await handler.generate(lesson_id=lesson_id, instructor_username="teacher1")

    assert result.lesson_id == lesson_id
    assert len(result.outline) == 2
    assert result.outline[0].title == "Context & Objectives"


@pytest.mark.asyncio
async def test_expand_subtopic_resources_returns_curated_items():
    instructor_id = uuid4()
    lesson_id = uuid4()
    subtopic = "Invention of the telescope"

    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        get_for_instructor=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                audience="high school",
                resource_recommendations={},
            )
        ),
        update_generated_content=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                resource_recommendations={
                    subtopic: [
                        {
                            "title": "Britannica overview",
                            "url": "https://www.britannica.com",
                            "source": "Encyclopaedia Britannica",
                            "resource_type": "reference",
                            "rationale": "Baseline",
                        }
                    ]
                },
            )
        ),
    )

    handler = LessonExpandSubtopicResourcesCommandHandler(db)
    result = await handler.expand(
        lesson_id=lesson_id,
        subtopic=subtopic,
        instructor_username="teacher1",
    )

    assert result.lesson_id == lesson_id
    assert result.subtopic == subtopic
    assert len(result.resources) == 1
    assert result.resources[0].source == "Encyclopaedia Britannica"


@pytest.mark.asyncio
async def test_get_lesson_project_includes_phase2_content():
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
                status="draft",
                instructor_user_id=instructor_id,
                review_notes=None,
                created_at=None,
                updated_at=None,
                outline=[{"title": "Context & Objectives", "bullets": ["b1"]}],
                resource_recommendations={
                    "Telescope": [
                        {
                            "title": "Britannica overview",
                            "url": "https://www.britannica.com",
                            "source": "Encyclopaedia Britannica",
                            "resource_type": "reference",
                            "rationale": "Baseline",
                        }
                    ]
                },
            )
        )
    )

    handler = GetLessonProjectQueryHandler(db)
    result = await handler.get(lesson_id=lesson_id, instructor_username="teacher1")

    assert result.outline is not None
    assert result.outline[0].title == "Context & Objectives"
    assert "Telescope" in (result.resource_recommendations or {})

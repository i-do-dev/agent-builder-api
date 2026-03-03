from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import AsyncMock
import pytest

from src.handlers.commands.lesson.summarize_content import LessonSummarizeContentCommandHandler
from src.handlers.commands.lesson.generate_assessment import LessonGenerateAssessmentCommandHandler
from src.handlers.errors import ValidationError


@pytest.mark.asyncio
async def test_summarize_content_persists_summary():
    instructor_id = uuid4()
    lesson_id = uuid4()

    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        get_for_instructor=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                topic="Scientific Revolution",
                instructional_focus="major inventions",
            )
        ),
        update_generated_content=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                summary={
                    "source_url": "https://example.org",
                    "key_points": ["k1", "k2"],
                    "extracted_parameters": ["focal length"],
                    "concise_summary": "short summary",
                },
            )
        ),
    )

    handler = LessonSummarizeContentCommandHandler(db)
    result = await handler.summarize(
        lesson_id=lesson_id,
        instructor_username="teacher1",
        source_text="Sample text about telescope design and focal length.",
        source_url="https://example.org",
    )

    assert result.lesson_id == lesson_id
    assert result.summary.source_url == "https://example.org"
    assert len(result.summary.key_points) >= 1


@pytest.mark.asyncio
async def test_summarize_content_requires_input():
    instructor_id = uuid4()
    lesson_id = uuid4()

    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(get_for_instructor=AsyncMock(), update_generated_content=AsyncMock())

    handler = LessonSummarizeContentCommandHandler(db)

    with pytest.raises(ValidationError):
        await handler.summarize(
            lesson_id=lesson_id,
            instructor_username="teacher1",
            source_text=None,
            source_url=None,
        )


@pytest.mark.asyncio
async def test_generate_assessment_persists_questions():
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
                summary={"key_points": ["Key concept"]},
            )
        ),
        update_generated_content=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                assessments=[
                    {
                        "question": "Q1",
                        "options": ["A", "B", "C", "D"],
                        "answer": "A",
                        "rationale": "Because",
                    }
                ],
            )
        ),
    )

    handler = LessonGenerateAssessmentCommandHandler(db)
    result = await handler.generate(
        lesson_id=lesson_id,
        instructor_username="teacher1",
        question_count=1,
    )

    assert result.lesson_id == lesson_id
    assert len(result.questions) == 1
    assert result.questions[0].question == "Q1"

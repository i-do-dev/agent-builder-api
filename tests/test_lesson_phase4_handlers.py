from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import AsyncMock
import pytest

from src.core.entities.lesson import LessonStatus
from src.handlers.commands.lesson.apply_approval_decision import LessonApprovalDecisionCommandHandler
from src.handlers.commands.lesson.generate_thematic_map import LessonGenerateThematicMapCommandHandler
from src.handlers.commands.lesson.submit_for_review import LessonSubmitForReviewCommandHandler
from src.handlers.errors import ValidationError


@pytest.mark.asyncio
async def test_generate_thematic_mapping_persists_and_returns_items():
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
                thematic_mapping=[
                    {
                        "concept": "Empirical methods",
                        "societal_impact": "Intellectual freedom",
                        "explanation": "Reasoning shifted to evidence-based inquiry.",
                    }
                ],
            )
        ),
    )

    handler = LessonGenerateThematicMapCommandHandler(db)
    result = await handler.generate(
        lesson_id=lesson_id,
        instructor_username="teacher1",
        cross_disciplinary_focus="human rights",
    )

    assert result.lesson_id == lesson_id
    assert result.cross_disciplinary_focus == "human rights"
    assert len(result.mapping) == 1
    assert result.mapping[0].societal_impact == "Intellectual freedom"


@pytest.mark.asyncio
async def test_edit_decision_moves_to_needs_revision():
    instructor_id = uuid4()
    lesson_id = uuid4()

    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        get_for_instructor=AsyncMock(return_value=SimpleNamespace(id=lesson_id, status=LessonStatus.IN_REVIEW)),
        update_status=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                topic="Scientific Revolution",
                audience="high school",
                instructional_focus="major inventions",
                status=LessonStatus.NEEDS_REVISION,
                instructor_user_id=instructor_id,
                review_notes="Revise objectives",
                created_at=None,
                updated_at=None,
            )
        ),
    )

    handler = LessonApprovalDecisionCommandHandler(db)
    result = await handler.apply(
        lesson_id=lesson_id,
        decision="edit",
        instructor_username="teacher1",
        review_notes="Revise objectives",
    )

    assert result.status == LessonStatus.NEEDS_REVISION


@pytest.mark.asyncio
async def test_reject_or_edit_requires_review_notes():
    instructor_id = uuid4()
    lesson_id = uuid4()

    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        get_for_instructor=AsyncMock(return_value=SimpleNamespace(id=lesson_id, status=LessonStatus.IN_REVIEW)),
        update_status=AsyncMock(),
    )

    handler = LessonApprovalDecisionCommandHandler(db)

    with pytest.raises(ValidationError):
        await handler.apply(
            lesson_id=lesson_id,
            decision="edit",
            instructor_username="teacher1",
            review_notes="",
        )


@pytest.mark.asyncio
async def test_submit_for_review_accepts_needs_revision():
    instructor_id = uuid4()
    lesson_id = uuid4()

    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        get_for_instructor=AsyncMock(
            return_value=SimpleNamespace(id=lesson_id, status=LessonStatus.NEEDS_REVISION, review_notes="Please revise")
        ),
        update_status=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                topic="Scientific Revolution",
                audience="high school",
                instructional_focus="major inventions",
                status=LessonStatus.IN_REVIEW,
                instructor_user_id=instructor_id,
                review_notes="Please revise",
                created_at=None,
                updated_at=None,
            )
        ),
    )

    handler = LessonSubmitForReviewCommandHandler(db)
    result = await handler.submit(lesson_id=lesson_id, instructor_username="teacher1")

    assert result.status == LessonStatus.IN_REVIEW

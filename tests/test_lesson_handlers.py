from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import AsyncMock
import pytest

from src.core.entities.lesson import LessonStatus
from src.handlers.commands.lesson.create_lesson_project import LessonCreateCommandHandler
from src.handlers.commands.lesson.submit_for_review import LessonSubmitForReviewCommandHandler
from src.handlers.commands.lesson.apply_approval_decision import LessonApprovalDecisionCommandHandler
from src.handlers.contracts.lesson import LessonCreateCommand
from src.handlers.errors import NotFoundError, ValidationError


@pytest.mark.asyncio
async def test_create_lesson_project_success():
    instructor_id = uuid4()
    lesson_id = uuid4()
    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        add=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                topic="Scientific Revolution",
                audience="high school",
                instructional_focus="major inventions",
                status=LessonStatus.DRAFT,
                instructor_user_id=instructor_id,
                review_notes=None,
                created_at=None,
                updated_at=None,
            )
        )
    )

    handler = LessonCreateCommandHandler(db)
    result = await handler.create_on_request(
        LessonCreateCommand(
            topic="Scientific Revolution",
            audience="high school",
            instructional_focus="major inventions",
        ),
        instructor_username="teacher1",
    )

    assert result.id == lesson_id
    assert result.status == LessonStatus.DRAFT
    assert result.instructor_user_id == instructor_id


@pytest.mark.asyncio
async def test_submit_for_review_requires_draft():
    instructor_id = uuid4()
    lesson_id = uuid4()
    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        get_for_instructor=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                status=LessonStatus.APPROVED,
                review_notes=None,
            )
        )
    )

    handler = LessonSubmitForReviewCommandHandler(db)

    with pytest.raises(ValidationError):
        await handler.submit(lesson_id=lesson_id, instructor_username="teacher1")


@pytest.mark.asyncio
async def test_apply_approval_decision_happy_path():
    instructor_id = uuid4()
    lesson_id = uuid4()
    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=SimpleNamespace(id=instructor_id)))
    db.lesson = SimpleNamespace(
        get_for_instructor=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                status=LessonStatus.IN_REVIEW,
            )
        ),
        update_status=AsyncMock(
            return_value=SimpleNamespace(
                id=lesson_id,
                topic="Scientific Revolution",
                audience="high school",
                instructional_focus="major inventions",
                status=LessonStatus.APPROVED,
                instructor_user_id=instructor_id,
                review_notes="Looks good",
                created_at=None,
                updated_at=None,
            )
        ),
    )

    handler = LessonApprovalDecisionCommandHandler(db)
    result = await handler.apply(
        lesson_id=lesson_id,
        decision="approve",
        instructor_username="teacher1",
        review_notes="Looks good",
    )

    assert result.status == LessonStatus.APPROVED
    assert result.review_notes == "Looks good"


@pytest.mark.asyncio
async def test_apply_approval_decision_instructor_not_found():
    lesson_id = uuid4()
    db = SimpleNamespace()
    db.user = SimpleNamespace(get_by_username=AsyncMock(return_value=None))
    db.lesson = SimpleNamespace(get_for_instructor=AsyncMock(), update_status=AsyncMock())

    handler = LessonApprovalDecisionCommandHandler(db)

    with pytest.raises(NotFoundError):
        await handler.apply(
            lesson_id=lesson_id,
            decision="approve",
            instructor_username="missing-teacher",
        )

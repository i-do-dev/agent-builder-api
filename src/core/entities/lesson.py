from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Any


class LessonStatus:
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class LessonProject:
    id: UUID | None = field(default=None)
    topic: str | None = field(default=None)
    audience: str | None = field(default=None)
    instructional_focus: str | None = field(default=None)
    status: str = field(default=LessonStatus.DRAFT)
    review_notes: str | None = field(default=None)
    instructor_user_id: UUID | None = field(default=None)
    outline: list[dict[str, Any]] | None = field(default=None)
    resource_recommendations: dict[str, list[dict[str, Any]]] | None = field(default=None)
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)

    def submit_for_review(self) -> None:
        if self.status != LessonStatus.DRAFT:
            raise ValueError("Only draft lessons can be submitted for review")
        self.status = LessonStatus.IN_REVIEW

    def approve(self, notes: str | None = None) -> None:
        if self.status != LessonStatus.IN_REVIEW:
            raise ValueError("Only in-review lessons can be approved")
        self.status = LessonStatus.APPROVED
        self.review_notes = notes

    def reject(self, notes: str | None = None) -> None:
        if self.status != LessonStatus.IN_REVIEW:
            raise ValueError("Only in-review lessons can be rejected")
        self.status = LessonStatus.REJECTED
        self.review_notes = notes

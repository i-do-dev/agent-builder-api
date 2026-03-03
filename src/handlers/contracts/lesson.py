from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass(frozen=True)
class LessonCreateCommand:
    topic: str
    audience: str
    instructional_focus: str


@dataclass(frozen=True)
class LessonSubmitForReviewCommand:
    lesson_id: UUID


@dataclass(frozen=True)
class LessonApprovalDecisionCommand:
    lesson_id: UUID
    decision: str
    review_notes: Optional[str] = None


@dataclass(frozen=True)
class LessonResult:
    id: UUID
    topic: str
    audience: str
    instructional_focus: str
    status: str
    instructor_user_id: UUID
    review_notes: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    outline: Optional[list["OutlineSectionResult"]] = None
    resource_recommendations: Optional[dict[str, list["ResourceRecommendationResult"]]] = None


@dataclass(frozen=True)
class OutlineSectionResult:
    title: str
    bullets: list[str]


@dataclass(frozen=True)
class ResourceRecommendationResult:
    title: str
    url: str
    source: str
    resource_type: str
    rationale: str


@dataclass(frozen=True)
class LessonOutlineResult:
    lesson_id: UUID
    outline: list[OutlineSectionResult]


@dataclass(frozen=True)
class LessonSubtopicResourcesResult:
    lesson_id: UUID
    subtopic: str
    resources: list[ResourceRecommendationResult]

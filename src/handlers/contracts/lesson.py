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
    summary: Optional["SummaryResult"] = None
    assessments: Optional[list["AssessmentQuestionResult"]] = None


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


@dataclass(frozen=True)
class LessonSummarizeContentCommand:
    lesson_id: UUID
    source_text: str | None = None
    source_url: str | None = None


@dataclass(frozen=True)
class SummaryResult:
    source_url: str | None
    key_points: list[str]
    extracted_parameters: list[str]
    concise_summary: str


@dataclass(frozen=True)
class LessonSummaryResult:
    lesson_id: UUID
    summary: SummaryResult


@dataclass(frozen=True)
class LessonGenerateAssessmentCommand:
    lesson_id: UUID
    question_count: int = 10


@dataclass(frozen=True)
class AssessmentQuestionResult:
    question: str
    options: list[str]
    answer: str
    rationale: str


@dataclass(frozen=True)
class LessonAssessmentResult:
    lesson_id: UUID
    questions: list[AssessmentQuestionResult]

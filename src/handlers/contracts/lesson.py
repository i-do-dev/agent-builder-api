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
    thematic_mapping: Optional[list["ThematicMappingItemResult"]] = None


@dataclass(frozen=True)
class LessonListResult:
    lessons: list["LessonResult"]
    page: int
    page_size: int
    total: int
    total_pages: int


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


@dataclass(frozen=True)
class LessonGenerateThematicMapCommand:
    lesson_id: UUID
    cross_disciplinary_focus: str


@dataclass(frozen=True)
class ThematicMappingItemResult:
    concept: str
    societal_impact: str
    explanation: str


@dataclass(frozen=True)
class LessonThematicMapResult:
    lesson_id: UUID
    cross_disciplinary_focus: str
    mapping: list[ThematicMappingItemResult]


@dataclass(frozen=True)
class DeepAgentRunCommand:
    prompt: str
    subtopic: Optional[str] = None
    source_text: Optional[str] = None
    source_url: Optional[str] = None
    question_count: int = 10
    cross_disciplinary_focus: Optional[str] = None
    execute: bool = True


@dataclass(frozen=True)
class DeepAgentRunResult:
    lesson_id: UUID
    intent: str
    todos: list[str]
    executed: bool
    actions_taken: list[str]
    outline_sections: int = 0
    resource_count: int = 0
    summary_generated: bool = False
    assessment_count: int = 0
    thematic_mapping_count: int = 0

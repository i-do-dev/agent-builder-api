from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class OutlineSectionResponse(BaseModel):
    title: str
    bullets: list[str]


class ResourceRecommendationResponse(BaseModel):
    title: str
    url: str
    source: str
    resource_type: str
    rationale: str


class LessonOutlineResponse(BaseModel):
    lesson_id: UUID
    outline: list[OutlineSectionResponse]


class LessonSubtopicResourcesResponse(BaseModel):
    lesson_id: UUID
    subtopic: str
    resources: list[ResourceRecommendationResponse]


class SummaryResponse(BaseModel):
    source_url: Optional[str] = None
    key_points: list[str]
    extracted_parameters: list[str]
    concise_summary: str


class LessonSummaryResponse(BaseModel):
    lesson_id: UUID
    summary: SummaryResponse


class AssessmentQuestionResponse(BaseModel):
    question: str
    options: list[str]
    answer: str
    rationale: str


class LessonAssessmentResponse(BaseModel):
    lesson_id: UUID
    questions: list[AssessmentQuestionResponse]


class ThematicMappingItemResponse(BaseModel):
    concept: str
    societal_impact: str
    explanation: str


class LessonThematicMapResponse(BaseModel):
    lesson_id: UUID
    cross_disciplinary_focus: str
    mapping: list[ThematicMappingItemResponse]


class DeepAgentRunResponse(BaseModel):
    lesson_id: UUID
    intent: str
    todos: list[str]
    executed: bool
    actions_taken: list[str]
    outline_sections: int
    resource_count: int
    summary_generated: bool
    assessment_count: int
    thematic_mapping_count: int


class LessonResponse(BaseModel):
    id: UUID
    topic: str
    audience: str
    instructional_focus: str
    status: str
    instructor_user_id: UUID
    review_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    outline: Optional[list[OutlineSectionResponse]] = None
    resource_recommendations: Optional[dict[str, list[ResourceRecommendationResponse]]] = None
    summary: Optional[SummaryResponse] = None
    assessments: Optional[list[AssessmentQuestionResponse]] = None
    thematic_mapping: Optional[list[ThematicMappingItemResponse]] = None

    class Config:
        from_attributes = True

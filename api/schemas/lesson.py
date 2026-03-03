from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Literal


class LessonCreateRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=255)
    audience: str = Field(..., min_length=2, max_length=128)
    instructional_focus: str = Field(..., min_length=3)


class LessonReviewDecisionRequest(BaseModel):
    decision: Literal["approve", "reject", "edit"]
    review_notes: Optional[str] = None


class LessonSubtopicResourcesRequest(BaseModel):
    subtopic: str = Field(..., min_length=2, max_length=255)


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

    class Config:
        from_attributes = True

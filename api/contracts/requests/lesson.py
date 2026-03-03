from pydantic import BaseModel, Field
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


class LessonSummarizeRequest(BaseModel):
    source_text: Optional[str] = None
    source_url: Optional[str] = None


class LessonAssessmentRequest(BaseModel):
    question_count: int = Field(default=10, ge=1, le=20)


class LessonThematicMapRequest(BaseModel):
    cross_disciplinary_focus: str = Field(..., min_length=3)


class DeepAgentRunRequest(BaseModel):
    prompt: str = Field(..., min_length=3)
    subtopic: Optional[str] = None
    source_text: Optional[str] = None
    source_url: Optional[str] = None
    question_count: int = Field(default=10, ge=1, le=20)
    cross_disciplinary_focus: Optional[str] = None
    execute: bool = True

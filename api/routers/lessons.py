from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from api.dependencies.common import BearerToken, TokenSvc
from api.dependencies.lesson import (
    LessonAssessmentHandlerDep,
    LessonApprovalHandlerDep,
    LessonCreateHandlerDep,
    LessonExpandSubtopicResourcesHandlerDep,
    LessonGenerateOutlineHandlerDep,
    LessonQueryHandlerDep,
    LessonSummarizeHandlerDep,
    LessonSubmitReviewHandlerDep,
)
from api.schemas.auth import TokenPayload
from api.schemas.lesson import (
    LessonAssessmentRequest,
    LessonAssessmentResponse,
    LessonCreateRequest,
    LessonOutlineResponse,
    LessonResponse,
    LessonReviewDecisionRequest,
    LessonSummarizeRequest,
    LessonSummaryResponse,
    LessonSubtopicResourcesRequest,
    LessonSubtopicResourcesResponse,
)
from src.handlers.errors import NotFoundError, ValidationError
from src.handlers.mappers.lesson import LessonApiMapper

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"],
)


@router.post("/", response_model=LessonResponse)
async def create_lesson(
    bearer_token: BearerToken,
    token_svc: TokenSvc,
    handler: LessonCreateHandlerDep,
    request: LessonCreateRequest,
) -> LessonResponse:
    token_payload: TokenPayload = token_svc.decode(bearer_token)
    command = LessonApiMapper.request_to_create_command(request)
    try:
        result = await handler.create_on_request(command, token_payload.sub)
        return LessonApiMapper.result_to_response(result)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: UUID,
    bearer_token: BearerToken,
    token_svc: TokenSvc,
    query: LessonQueryHandlerDep,
) -> LessonResponse:
    token_payload: TokenPayload = token_svc.decode(bearer_token)
    try:
        result = await query.get(lesson_id, token_payload.sub)
        return LessonApiMapper.result_to_response(result)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{lesson_id}/submit-review", response_model=LessonResponse)
async def submit_for_review(
    lesson_id: UUID,
    bearer_token: BearerToken,
    token_svc: TokenSvc,
    handler: LessonSubmitReviewHandlerDep,
) -> LessonResponse:
    token_payload: TokenPayload = token_svc.decode(bearer_token)
    try:
        result = await handler.submit(lesson_id, token_payload.sub)
        return LessonApiMapper.result_to_response(result)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{lesson_id}/review", response_model=LessonResponse)
async def apply_review_decision(
    lesson_id: UUID,
    request: LessonReviewDecisionRequest,
    bearer_token: BearerToken,
    token_svc: TokenSvc,
    handler: LessonApprovalHandlerDep,
) -> LessonResponse:
    token_payload: TokenPayload = token_svc.decode(bearer_token)
    try:
        result = await handler.apply(
            lesson_id=lesson_id,
            decision=request.decision,
            review_notes=request.review_notes,
            instructor_username=token_payload.sub,
        )
        return LessonApiMapper.result_to_response(result)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{lesson_id}/outline", response_model=LessonOutlineResponse)
async def generate_outline(
    lesson_id: UUID,
    bearer_token: BearerToken,
    token_svc: TokenSvc,
    handler: LessonGenerateOutlineHandlerDep,
) -> LessonOutlineResponse:
    token_payload: TokenPayload = token_svc.decode(bearer_token)
    try:
        result = await handler.generate(lesson_id=lesson_id, instructor_username=token_payload.sub)
        return LessonApiMapper.outline_result_to_response(result)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{lesson_id}/subtopic-resources", response_model=LessonSubtopicResourcesResponse)
async def expand_subtopic_resources(
    lesson_id: UUID,
    request: LessonSubtopicResourcesRequest,
    bearer_token: BearerToken,
    token_svc: TokenSvc,
    handler: LessonExpandSubtopicResourcesHandlerDep,
) -> LessonSubtopicResourcesResponse:
    token_payload: TokenPayload = token_svc.decode(bearer_token)
    try:
        result = await handler.expand(
            lesson_id=lesson_id,
            subtopic=request.subtopic,
            instructor_username=token_payload.sub,
        )
        return LessonApiMapper.subtopic_resources_result_to_response(result)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{lesson_id}/summary", response_model=LessonSummaryResponse)
async def summarize_content(
    lesson_id: UUID,
    request: LessonSummarizeRequest,
    bearer_token: BearerToken,
    token_svc: TokenSvc,
    handler: LessonSummarizeHandlerDep,
) -> LessonSummaryResponse:
    token_payload: TokenPayload = token_svc.decode(bearer_token)
    try:
        result = await handler.summarize(
            lesson_id=lesson_id,
            instructor_username=token_payload.sub,
            source_text=request.source_text,
            source_url=request.source_url,
        )
        return LessonApiMapper.summary_result_to_response(result)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{lesson_id}/assessment", response_model=LessonAssessmentResponse)
async def generate_assessment(
    lesson_id: UUID,
    request: LessonAssessmentRequest,
    bearer_token: BearerToken,
    token_svc: TokenSvc,
    handler: LessonAssessmentHandlerDep,
) -> LessonAssessmentResponse:
    token_payload: TokenPayload = token_svc.decode(bearer_token)
    try:
        result = await handler.generate(
            lesson_id=lesson_id,
            instructor_username=token_payload.sub,
            question_count=request.question_count,
        )
        return LessonApiMapper.assessment_result_to_response(result)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

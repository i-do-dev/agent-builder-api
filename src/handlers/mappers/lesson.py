from api.schemas.lesson import (
    AssessmentQuestionResponse,
    LessonAssessmentResponse,
    LessonCreateRequest,
    LessonOutlineResponse,
    LessonResponse,
    LessonSummaryResponse,
    LessonSubtopicResourcesResponse,
    OutlineSectionResponse,
    ResourceRecommendationResponse,
    SummaryResponse,
)
from src.handlers.contracts.lesson import (
    LessonAssessmentResult,
    LessonCreateCommand,
    LessonOutlineResult,
    LessonResult,
    LessonSummaryResult,
    LessonSubtopicResourcesResult,
)


class LessonApiMapper:
    @staticmethod
    def request_to_create_command(request: LessonCreateRequest) -> LessonCreateCommand:
        return LessonCreateCommand(
            topic=request.topic,
            audience=request.audience,
            instructional_focus=request.instructional_focus,
        )

    @staticmethod
    def result_to_response(result: LessonResult) -> LessonResponse:
        outline = None
        if result.outline is not None:
            outline = [
                OutlineSectionResponse(title=section.title, bullets=section.bullets)
                for section in result.outline
            ]

        resource_recommendations = None
        if result.resource_recommendations is not None:
            resource_recommendations = {
                subtopic: [
                    ResourceRecommendationResponse(
                        title=item.title,
                        url=item.url,
                        source=item.source,
                        resource_type=item.resource_type,
                        rationale=item.rationale,
                    )
                    for item in items
                ]
                for subtopic, items in result.resource_recommendations.items()
            }

        summary = None
        if result.summary is not None:
            summary = SummaryResponse(
                source_url=result.summary.source_url,
                key_points=result.summary.key_points,
                extracted_parameters=result.summary.extracted_parameters,
                concise_summary=result.summary.concise_summary,
            )

        assessments = None
        if result.assessments is not None:
            assessments = [
                AssessmentQuestionResponse(
                    question=item.question,
                    options=item.options,
                    answer=item.answer,
                    rationale=item.rationale,
                )
                for item in result.assessments
            ]

        return LessonResponse(
            id=result.id,
            topic=result.topic,
            audience=result.audience,
            instructional_focus=result.instructional_focus,
            status=result.status,
            instructor_user_id=result.instructor_user_id,
            review_notes=result.review_notes,
            created_at=result.created_at,
            updated_at=result.updated_at,
            outline=outline,
            resource_recommendations=resource_recommendations,
            summary=summary,
            assessments=assessments,
        )

    @staticmethod
    def outline_result_to_response(result: LessonOutlineResult) -> LessonOutlineResponse:
        return LessonOutlineResponse(
            lesson_id=result.lesson_id,
            outline=[
                OutlineSectionResponse(title=section.title, bullets=section.bullets)
                for section in result.outline
            ],
        )

    @staticmethod
    def subtopic_resources_result_to_response(
        result: LessonSubtopicResourcesResult,
    ) -> LessonSubtopicResourcesResponse:
        return LessonSubtopicResourcesResponse(
            lesson_id=result.lesson_id,
            subtopic=result.subtopic,
            resources=[
                ResourceRecommendationResponse(
                    title=item.title,
                    url=item.url,
                    source=item.source,
                    resource_type=item.resource_type,
                    rationale=item.rationale,
                )
                for item in result.resources
            ],
        )

    @staticmethod
    def summary_result_to_response(result: LessonSummaryResult) -> LessonSummaryResponse:
        return LessonSummaryResponse(
            lesson_id=result.lesson_id,
            summary=SummaryResponse(
                source_url=result.summary.source_url,
                key_points=result.summary.key_points,
                extracted_parameters=result.summary.extracted_parameters,
                concise_summary=result.summary.concise_summary,
            ),
        )

    @staticmethod
    def assessment_result_to_response(result: LessonAssessmentResult) -> LessonAssessmentResponse:
        return LessonAssessmentResponse(
            lesson_id=result.lesson_id,
            questions=[
                AssessmentQuestionResponse(
                    question=item.question,
                    options=item.options,
                    answer=item.answer,
                    rationale=item.rationale,
                )
                for item in result.questions
            ],
        )

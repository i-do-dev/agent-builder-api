from api.schemas.lesson import (
    LessonCreateRequest,
    LessonOutlineResponse,
    LessonResponse,
    LessonSubtopicResourcesResponse,
    OutlineSectionResponse,
    ResourceRecommendationResponse,
)
from src.handlers.contracts.lesson import (
    LessonCreateCommand,
    LessonOutlineResult,
    LessonResult,
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

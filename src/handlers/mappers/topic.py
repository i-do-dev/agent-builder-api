from api.schemas.topic import TopicCreateRequest, TopicResponse
from src.handlers.contracts.topic import TopicCreateCommand, TopicResult


class TopicApiMapper:
    @staticmethod
    def request_to_command(request: TopicCreateRequest) -> TopicCreateCommand:
        return TopicCreateCommand(
            label=request.label,
            classification_description=request.classification_description,
            instructions=request.instructions or [],
        )

    @staticmethod
    def result_to_response(result: TopicResult) -> TopicResponse:
        return TopicResponse(
            id=result.id,
            label=result.label,
            classification_description=result.classification_description,
            instructions=result.instructions,
            agent=result.agent,
        )

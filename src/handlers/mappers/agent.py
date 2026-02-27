from api.schemas.agent import AgentCreateRequest, AgentResponse
from src.handlers.contracts.agent import AgentCreateCommand, AgentResult


class AgentApiMapper:
    @staticmethod
    def request_to_command(request: AgentCreateRequest) -> AgentCreateCommand:
        return AgentCreateCommand(
            name=request.name,
            api_name=request.api_name,
            description=request.description,
            role=request.role,
            organization=request.organization,
            user_type=request.user_type,
        )

    @staticmethod
    def result_to_response(result: AgentResult) -> AgentResponse:
        return AgentResponse(
            id=result.id,
            name=result.name,
            api_name=result.api_name,
            description=result.description,
            role=result.role,
            organization=result.organization,
            user_type=result.user_type,
            modified_by=result.modified_by,
            topics=result.topics,
        )

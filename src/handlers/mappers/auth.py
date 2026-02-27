from api.contracts.requests.user import UserSignUpRequest
from api.contracts.responses.user import UserProfileResponse, UserSignUpResponse
from api.contracts.token import Token
from src.handlers.contracts.auth import SignInResult, SignUpCommand, UserProfileResult


class AuthApiMapper:
    @staticmethod
    def signup_request_to_command(request: UserSignUpRequest) -> SignUpCommand:
        return SignUpCommand(
            username=request.username,
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            password=request.password,
            confirm_password=request.confirm_password,
        )

    @staticmethod
    def profile_result_to_signup_response(result: UserProfileResult) -> UserSignUpResponse:
        return UserSignUpResponse(
            username=result.username,
            email=result.email,
            first_name=result.first_name,
            last_name=result.last_name,
            joined_at=result.joined_at,
        )

    @staticmethod
    def profile_result_to_profile_response(result: UserProfileResult) -> UserProfileResponse:
        return UserProfileResponse(
            username=result.username,
            email=result.email,
            first_name=result.first_name,
            last_name=result.last_name,
            joined_at=result.joined_at,
        )

    @staticmethod
    def signin_result_to_token(result: SignInResult) -> Token:
        return Token(access_token=result.access_token, token_type=result.token_type)

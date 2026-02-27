from dataclasses import dataclass


@dataclass(frozen=True)
class SignInCommand:
    identifier: str
    password: str


@dataclass(frozen=True)
class SignInResult:
    access_token: str
    token_type: str = "bearer"


@dataclass(frozen=True)
class SignUpCommand:
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    confirm_password: str


@dataclass(frozen=True)
class UserProfileResult:
    username: str
    email: str
    first_name: str
    last_name: str
    joined_at: str | None = None

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional


@dataclass(frozen=True)
class TokenPayload:
    sub: str
    exp: int


class ITokenHandler(ABC):
    @abstractmethod
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        pass

    @abstractmethod
    def decode(self, token: str) -> TokenPayload:
        pass

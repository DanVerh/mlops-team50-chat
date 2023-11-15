from html import escape
from typing import Annotated

from pydantic import BaseModel, Field, validator


class UserName(BaseModel):
    username: Annotated[str, Field(min_length=1, pattern=r"^[a-zA-Z0-9_]+$")]

    @validator("username", pre=True, allow_reuse=True)
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class Message(BaseModel):
    content: Annotated[str, Field(min_length=1)]

    @validator("content", pre=True, allow_reuse=True)
    def sanitize_content(cls, v: str) -> str:
        # Sanitize the content to prevent XSS attacks
        return escape(v.strip())


class CensorRequest(BaseModel):
    text: str

# pylint: disable=no-name-in-module
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, validator


class Method(str, Enum):
    get = "GET"
    head = "HEAD"
    post = "POST"
    put = "PUT"
    delete = "DELETE"
    options = "OPTIONS"
    trace = "TRACE"
    patch = "PATCH"


class Endpoint(BaseModel):
    method: Method
    path: str
    status_code: int
    media_type: str = "application/json"
    content: Optional[str]
    content_path: Optional[str]

    @validator("content_path", pre=True, always=True)
    def content_path_correct(cls, value, values):  # pylint:disable=no-self-argument, no-self-use
        if values["content"] is not None and value is not None:
            raise ValueError("Cannot set both content and content_path.")
        return value


class ContentFunction(BaseModel):
    full: str
    name: str
    params: List[str]

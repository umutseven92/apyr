# pylint: disable=no-name-in-module
from enum import Enum
from typing import Optional, Callable

from pydantic import BaseModel


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


class ContentFunction(BaseModel):
    name: str
    returns: Callable[[], str]

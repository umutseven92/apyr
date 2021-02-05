# pylint: disable=no-name-in-module
from enum import Enum
from typing import Optional, Callable

from pydantic import BaseModel


class Method(str, Enum):
    get = ("GET",)
    post = ("POST",)
    put = ("PUT",)
    delete = "DELETE"


class Endpoint(BaseModel):
    method: Method
    path: str
    status_code: int
    media_type: str = "application/json"
    content: Optional[str]


class ContentFunction(BaseModel):
    name: str
    returns: Callable[[], str]

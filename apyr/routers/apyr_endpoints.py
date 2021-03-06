""" Endpoints used by apyr itself.

Prefixed by `/apyr` so as to not block user defined endpoints from being mocked.
"""
from fastapi import APIRouter

from starlette.responses import Response
from starlette.status import HTTP_200_OK

apyr_router = APIRouter(prefix="/apyr")


@apyr_router.get("/status")
async def status():
    """Status check for the apyr service. Used mainly as a health check."""
    return Response(status_code=HTTP_200_OK)

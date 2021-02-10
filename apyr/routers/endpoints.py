from functools import lru_cache

from fastapi import APIRouter, Depends, Request, HTTPException

from apyr.dependencies import EndpointsRepo
from apyr.exceptions import EndpointException

endpoint_router = APIRouter()


@lru_cache
def endpoints_dependency() -> EndpointsRepo:
    return EndpointsRepo()


@endpoint_router.get("/{path:path}")
@endpoint_router.head("/{path:path}")
@endpoint_router.post("/{path:path}")
@endpoint_router.put("/{path:path}")
@endpoint_router.delete("/{path:path}")
@endpoint_router.options("/{path:path}")
@endpoint_router.trace("/{path:path}")
@endpoint_router.patch("/{path:path}")
async def all_endpoints(
        path: str, request: Request, repo: EndpointsRepo = Depends(endpoints_dependency)
):
    try:
        response = repo.get_response(path, request.method)
    except EndpointException as ex:
        raise HTTPException(status_code=404, detail=str(ex)) from ex

    return response

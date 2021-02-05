from fastapi import APIRouter, Depends, Request, HTTPException

from dependencies import EndpointsRepo
from exceptions import EndpointException

router = APIRouter()


@router.get("/{path:path}")
@router.post("/{path:path}")
@router.put("/{path:path}")
@router.delete("/{path:path}")
async def all_endpoints(
        path: str, request: Request, repo: EndpointsRepo = Depends(EndpointsRepo)
):
    try:
        response = repo.get_response(path, request.method)
    except EndpointException as ex:
        raise HTTPException(status_code=404, detail=str(ex)) from ex

    return response

from pathlib import Path
from typing import List

import yaml
from fastapi import HTTPException
from starlette.responses import Response

from apyr.exceptions import (
    TooManyEndpointsException,
    NoEndpointsException,
    FunctionException,
)
from apyr.function_handler import FunctionHandler
from apyr.functions import FUNCTIONS
from apyr.models import Endpoint
from apyr.utils import get_project_root, get_digest


class EndpointsRepo:
    def __init__(self):
        self.last_hash: str = ""
        self.endpoints: List[Endpoint] = []
        self.endpoints_path = get_project_root().joinpath("endpoints.yaml")

    def _load_endpoints(self):
        stream = open(self.endpoints_path, "r")
        endpoints = yaml.full_load(stream)

        self.endpoints = [Endpoint(**endpoint) for endpoint in endpoints]

    def _check_if_file_changed(self, path: Path) -> bool:
        """Check to see if the file changed.

        We hash the file and compare it to the previous hash.
        """
        new_hash = get_digest(str(path))
        if new_hash != self.last_hash:
            self.last_hash = new_hash
            return True

        return False

    def get_response(self, path: str, method: str) -> Response:
        # Do not reload endpoints if the file has not changed
        if self._check_if_file_changed(self.endpoints_path):
            self._load_endpoints()

        def _filter_endpoints(endpoint: Endpoint):
            return endpoint.path == path and endpoint.method.lower() == method.lower()

        filtered: List[Endpoint] = list(filter(_filter_endpoints, self.endpoints))

        if len(filtered) > 1:
            raise TooManyEndpointsException()
        if len(filtered) == 0:
            raise NoEndpointsException()

        filtered_endpoint = filtered[0]

        try:
            content = FunctionHandler.run(filtered_endpoint.content, FUNCTIONS)
        except FunctionException as ex:
            raise HTTPException(
                status_code=500, detail={"error": ex.error, "reason": ex.detail}
            ) from ex

        return Response(
            status_code=filtered_endpoint.status_code,
            media_type=filtered_endpoint.media_type,
            content=content,
        )

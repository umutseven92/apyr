from typing import List

import names
import yaml
from starlette.responses import Response

from exceptions import TooManyEndpointsException, NoEndpointsException
from models import Endpoint, ContentFunction
from utils import get_project_root

FUNCTIONS = [
    ContentFunction(name="random_first_name", returns=names.get_first_name),
    ContentFunction(name="random_last_name", returns=names.get_last_name),
]


class EndpointsRepo:
    def __init__(self):
        self._load_endpoints()

    def _load_endpoints(self):
        base_dir = get_project_root()
        endpoints_path = base_dir.joinpath("endpoints.yaml")
        stream = open(endpoints_path, "r")
        endpoints = yaml.full_load(stream)

        self.endpoints = [Endpoint(**endpoint) for endpoint in endpoints]

    @staticmethod
    def _check_for_functions(content: str) -> str:
        for function in FUNCTIONS:
            full_fun_name = f"%{function.name}%"
            if full_fun_name in content:
                return_val = function.returns()
                content = content.replace(full_fun_name, return_val)

        return content

    def get_response(self, path: str, method: str) -> Response:
        def _filter_endpoints(endpoint: Endpoint):
            return endpoint.path == path and endpoint.method.lower() == method.lower()

        filtered: List[Endpoint] = list(filter(_filter_endpoints, self.endpoints))

        if len(filtered) > 1:
            raise TooManyEndpointsException()
        if len(filtered) == 0:
            raise NoEndpointsException()

        filtered_endpoint = filtered[0]

        content = self._check_for_functions(filtered_endpoint.content)
        return Response(
            status_code=filtered_endpoint.status_code,
            media_type=filtered_endpoint.media_type,
            content=content,
        )

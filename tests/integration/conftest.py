from http.client import RemoteDisconnected

import pytest
import requests

from apyr.utils import get_project_root


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    del pytestconfig
    return get_project_root().joinpath("docker-compose.yaml")


@pytest.fixture(scope="session")
def apyr_service(docker_ip, docker_services):
    del docker_ip
    port = docker_services.port_for("apyr", 8000)
    base_url = f"http://0.0.0.0:{port}"

    def is_responsive():
        status_url = f"{base_url}/apyr/status"

        try:
            response = requests.get(status_url)
            if response.status_code == 200:
                return True
        except:
            return False

    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive()
    )
    return base_url

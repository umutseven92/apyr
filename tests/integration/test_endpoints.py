import re

import pytest
import requests


def strip_whitespace_html(content: str) -> str:
    """Strips whitespace from in-between HTML tags. Useful for when comparing HTML files."""
    return re.sub(r">\s*<", "><", content).strip()


class TestEndpoints:
    """Test class for the default `endpoints.yaml` file, which should cover all types of requests."""

    def test_get_employees(self, apyr_service):
        expected_body = [
            {"first_name": "Peter", "last_name": "Venkman"},
            {"first_name": "Ray", "last_name": "Stantz"},
            {"first_name": "Egon", "last_name": "Spengler"},
        ]
        response = requests.get(apyr_service + "/test/employees")

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"

        body = response.json()

        assert body == expected_body

    def test_get_employee(self, apyr_service):
        response = requests.get(apyr_service + "/test/employee/2")

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"

        body = response.json()

        assert "first_name" in body
        assert "last_name" in body
        assert "age" in body
        assert 20 <= body["age"] <= 50

    def test_post_employee(self, apyr_service):
        expected_body = "An unexpected error occurred while creating the employee."
        response = requests.post(apyr_service + "/test/employee")

        assert response.status_code == 500
        assert response.headers.get("content-type") == "text"

        body = response.text

        assert body == expected_body

    def test_put_employee(self, apyr_service):
        response = requests.put(apyr_service + "/test/employee/3")

        assert response.status_code == 201
        assert "content-type" not in response.headers
        assert response.text == ""

    @pytest.mark.parametrize("path", ["/test/help", "/test/help2"])
    def test_get_help(self, apyr_service, path: str):
        expected_body = """
            <!DOCTYPE html>
            <html>
              <body>
                <h1>I've quit better jobs than this.</h1>
                <p>Ghostbusters, whaddya want.</p>
              </body>
            </html>
        """

        response = requests.get(apyr_service + path)

        assert response.status_code == 200
        assert response.headers.get("content-type") == "text/html; charset=utf-8"

        body = response.text

        assert strip_whitespace_html(expected_body) == strip_whitespace_html(body)

import pytest

from apyr.models import Endpoint


class TestValidators:
    def test_setting_both_content_and_content_path_raises_value_error(self):
        endpoint_json = {
            "method": "POST",
            "path": "test/employee",
            "media_type": "text",
            "status_code": 500,
            "content": "Test",
            "content_path": "Test2",
        }

        with pytest.raises(ValueError):
            Endpoint(**endpoint_json)

    def test_setting_only_content_is_successful(self):
        endpoint_json = {
            "method": "POST",
            "path": "test/employee",
            "media_type": "text",
            "status_code": 500,
            "content": "Test",
        }

        endpoint = Endpoint(**endpoint_json)

        assert endpoint.content == "Test"
        assert endpoint.content_path is None

    def test_setting_only_content_path_is_successful(self):
        endpoint_json = {
            "method": "POST",
            "path": "test/employee",
            "media_type": "text",
            "status_code": 500,
            "content_path": "Test",
        }

        endpoint = Endpoint(**endpoint_json)

        assert endpoint.content_path == "Test"
        assert endpoint.content is None

    def test_setting_none_is_successful(self):
        endpoint_json = {
            "method": "POST",
            "path": "test/employee",
            "media_type": "text",
            "status_code": 500,
        }

        endpoint = Endpoint(**endpoint_json)

        assert endpoint.content_path is None
        assert endpoint.content is None

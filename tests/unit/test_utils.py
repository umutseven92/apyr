import os

import pytest

from apyr.utils import get_digest, get_project_root


class TestUtils:
    @pytest.mark.dependency(name="project_root")
    def test_can_get_project_root(self):
        base_dir = get_project_root()
        existing_path = base_dir.joinpath("pyproject.toml")

        assert os.path.isfile(existing_path)

    @pytest.mark.dependency(depends=["project_root"])
    def test_hash_same_file(self):
        string1_path = str(get_project_root().joinpath("tests/data/string1.txt"))

        initial_hash = get_digest(string1_path)
        duplicate_hash = get_digest(string1_path)

        assert initial_hash == duplicate_hash

    @pytest.mark.dependency(depends=["project_root"])
    def test_hash_diff_file(self):
        string1_path = str(get_project_root().joinpath("tests/data/string1.txt"))
        string2_path = str(get_project_root().joinpath("tests/data/string2.txt"))

        first_hash = get_digest(string1_path)
        second_hash = get_digest(string2_path)

        assert first_hash != second_hash

import hashlib
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_digest(file_path: str) -> str:
    hash_256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(hash_256.block_size)
            if not chunk:
                break
            hash_256.update(chunk)

    return hash_256.hexdigest()

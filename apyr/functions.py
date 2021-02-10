import random
from typing import Optional

import names


def random_first_name(gender: Optional[str]) -> str:
    return names.get_first_name(gender)


def random_last_name() -> str:
    return names.get_last_name()


def random_int(start: str, end: str) -> int:
    return random.randint(int(start), int(end))


FUNCTIONS = {
    "random_first_name": random_first_name,
    "random_last_name": random_last_name,
    "random_int": random_int,
}

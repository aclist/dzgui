import tomllib
from shared import get_git_root
from typing import Any


def get_entrypoint() -> Any:
    root = get_git_root()
    p = root.joinpath("pyproject.toml")
    with open(p, "rb") as f:
        t = tomllib.load(f)

    name = t["project"]["name"]
    return t["project"]["scripts"][name]

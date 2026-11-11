from dataclasses import dataclass
from typing import Callable

def immutable_dataclass(cls: type | None = None, **kwargs: bool) -> type | Callable[[type], type]:
    kwargs["slots"] = True
    kwargs["frozen"] = True
    if cls is None:
        return lambda c: dataclass(c, **kwargs)
    return dataclass(cls, **kwargs)

from collections.abc import Callable
from typing import Any
from pyexc._constants import EXCEPTION_ATTR

__all__ = ["get_exception_set"]


def get_exception_set(callable: Callable[..., Any]) -> set[type[BaseException]]:
    return getattr(callable, EXCEPTION_ATTR, set())

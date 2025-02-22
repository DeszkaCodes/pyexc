from collections.abc import Callable, Iterable
import functools
from typing import Any, ParamSpec, TypeVar

from pyexc._constants import EXCEPTION_ATTR
from pyexc._utils import get_exception_set

__all__ = ["raises"]


_P = ParamSpec("_P")
_R = TypeVar("_R")


def raises(exception: type[BaseException] | Iterable[type[BaseException]]) -> Callable[..., Any]:
    exception = set(exception) if isinstance(exception, Iterable) else {exception}

    return functools.partial(_raises_decorator, exception)


def _raises_decorator(
    exceptions: set[type[BaseException]], callable: Callable[_P, _R]
) -> Callable[_P, _R]:

    if not hasattr(callable, EXCEPTION_ATTR):
        setattr(callable, EXCEPTION_ATTR, set())

    get_exception_set(callable).update(exceptions)

    @functools.wraps(callable)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        return callable(*args, **kwargs)

    return wrapper

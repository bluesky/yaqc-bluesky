__all__ = ["callbacks_before_func", "callbacks_after_func"]

import functools
from dataclasses import dataclass
from typing import Any, List, Callable


@dataclass
class FunctionArgs:
    name: str
    host: str
    port: int
    args: list
    kwargs: dict


@dataclass
class FunctionResponse:
    name: str
    host: str
    port: int
    data: object


callbacks_before_func: List[Callable[[FunctionArgs], Amu]] = []

callbacks_after_func: List[Callable[[FunctionResponse], Any]]  = []




def with_func_callbacks(func):

    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        for cb in callbacks_before_func:
            message = FunctionCallbackItem(func.__qualname__, self.yaq_client._host, self.yaq_client._port, args=args, kwargs=kwargs)
            cb(message)
        out = func(self, *args, **kwargs)
        for cb in callbacks_after_func:
            response = FunctionCallbackItem(func.__qualname__, self.yaq_client._host, self.yaq_client_port, out)
        return out

    return inner


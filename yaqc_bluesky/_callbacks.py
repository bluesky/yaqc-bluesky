__all__ = ["callbacks_before_func", "callbacks_after_func"]


from dataclasses import dataclass


callbacks_before_func = []


callbacks_after_func = []


@dataclass
class FunctionArgs:
    name: str
    args: list
    kwargs: dict


@dataclass
class FunctionResponse:
    name: str
    data: object


def with_func_callbacks(func):

    def inner(*args, **kwargs):
        for cb in callbacks_before_func:
            message = FunctionCallbackItem(func.__name__, args=args, kwargs=kwargs)
            cb(message)
        out = func(*args, **kwargs)
        for cb in callbacks_after_func:
            response = FunctionCallbackItem(func.__name__, out)
        return out

    return inner


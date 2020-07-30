__all__ = [
    "YaqcBlueskyException",
    "InvalidState",
    "UnknownStatusFailure",
    "StatusTimeoutError",
    "WaitTimeoutError",
]


class YaqcBlueskyException(Exception):
    """
    yaqc-bluesky base exception class
    """

    pass


class InvalidState(RuntimeError, YaqcBlueskyException):
    """
    When Status.set_finished() or Status.set_exception(exc) is called too late
    """

    ...


class UnknownStatusFailure(YaqcBlueskyException):
    """
    Generic error when a Status object is marked success=False without details.
    """

    ...


class StatusTimeoutError(TimeoutError, YaqcBlueskyException):
    """
    Timeout specified when a Status object was created has expired.
    """

    ...


class UseNewProperty(RuntimeError, YaqcBlueskyException):
    ...


class WaitTimeoutError(TimeoutError, YaqcBlueskyException):
    """
    TimeoutError raised when we ware waiting on completion of a task.
    This is distinct from TimeoutError, just as concurrent.futures.TimeoutError
    is distinct from TimeoutError, to differentiate when the task itself has
    raised a TimeoutError.
    """

    ...

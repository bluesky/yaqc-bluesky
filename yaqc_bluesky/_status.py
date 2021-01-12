# mypy: ignore-errors

__all__ = ["Status"]


from collections import deque
import threading
from warnings import warn

from ._exceptions import (
    InvalidState,
    UnknownStatusFailure,
    StatusTimeoutError,
    WaitTimeoutError,
    UseNewProperty,
)


"""
The Status class has been adapted from ophyd:
https://github.com/bluesky/ophyd
The ophyd license is reproduced below:


Copyright (c) 2014, Brookhaven Science Associates, Brookhaven National
Laboratory. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the Brookhaven Science Associates, Brookhaven National
  Laboratory nor the names of its contributors may be used to endorse or promote
  products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


class Status:
    """
    Track the status of a potentially-lengthy action like moving or triggering.
    Parameters
    ----------
    timeout: float, optional
        The amount of time to wait before marking the Status as failed.  If
        ``None`` (default) wait forever. It is strongly encouraged to set a
        finite timeout.  If settle_time below is set, that time is added to the
        effective timeout.
    settle_time: float, optional
        The amount of time to wait between the caller specifying that the
        status has completed to running callbacks. Default is 0.
    Notes
    -----
    Theory of operation:
    This employs two ``threading.Event`` objects, one thread the runs for
    (timeout + settle_time) seconds, and one thread that runs for
    settle_time seconds (if settle_time is nonzero).
    At __init__ time, a *timeout* and *settle_time* are specified. A thread
    is started, on which user callbacks, registered after __init__ time via
    :meth:`add_callback`, will eventually be run. The thread waits on an
    Event be set or (timeout + settle_time) seconds to pass, whichever
    happens first.
    If (timeout + settle_time) expires and the Event has not
    been set, an internal Exception is set to ``StatusTimeoutError``, and a
    second Event is set, marking the Status as done and failed. The
    callbacks are run.
    If a callback is registered after the Status is done, it will be run
    immediately.
    If the first Event is set before (timeout + settle_time) expires,
    then the second Event is set and no internal Exception is set, marking
    the Status as done and successful. The callbacks are run.
    There are two methods that directly set the first Event. One,
    :meth:set_exception, sets it directly after setting the internal
    Exception.  The other, :meth:`set_finished`, starts a
    ``threading.Timer`` that will set it after a delay (the settle_time).
    One of these methods may be called, and at most once. If one is called
    twice or if both are called, ``InvalidState`` is raised. If they are
    called too late to prevent a ``StatusTimeoutError``, they are ignored
    but one call is still allowed. Thus, an external callback, e.g. pyepics,
    may reports success or failure after the Status object has expired, but
    to no effect because the callbacks have already been called and the
    program has moved on.
    """

    def __init__(self, *, timeout=None, settle_time=0, done=None, success=None):
        super().__init__()
        self._tname = None
        self._lock = threading.RLock()
        self._event = threading.Event()  # state associated with done-ness
        self._settled_event = threading.Event()
        # "Externally initiated" means set_finished() or set_exception(exc) was
        # called, as opposed to completion via an internal timeout.
        self._externally_initiated_completion_lock = threading.Lock()
        self._externally_initiated_completion = False
        self._callbacks = deque()
        self._exception = None

        if settle_time is None:
            settle_time = 0.0

        self._settle_time = float(settle_time)

        if timeout is not None:
            timeout = float(timeout)
        self._timeout = timeout

        # We cannot know that we are successful if we are not done.
        if success and not done:
            raise ValueError("Cannot initialize with done=False but success=True.")
        if done is not None or success is not None:
            warn(
                "The 'done' and 'success' parameters will be removed in a "
                "future release. Use the methods set_finished() or "
                "set_exception(exc) to mark success or failure, respectively, "
                "after the Status has been instantiated.",
                DeprecationWarning,
            )

        self._callback_thread = threading.Thread(
            target=self._run_callbacks, daemon=True, name=self._tname
        )
        self._callback_thread.start()

        if done:
            if success:
                self.set_finished()
            else:
                exc = UnknownStatusFailure(
                    f"The status {self!r} has failed. To obtain more specific, "
                    "helpful errors in the future, update the Device to use "
                    "set_exception(...) instead of setting success=False "
                    "at __init__ time."
                )
                self.set_exception(exc)

    @property
    def timeout(self):
        """
        The timeout for this action.
        This is set when the Status is created, and it cannot be changed.
        """
        return self._timeout

    @property
    def settle_time(self):
        """
        A delay between when :meth:`set_finished` is when the Status is done.
        This is set when the Status is created, and it cannot be changed.
        """
        return self._settle_time

    @property
    def done(self):
        """
        Boolean indicating whether associated operation has completed.
        This is set to True at __init__ time or by calling
        :meth:`set_finished`, :meth:`set_exception`, or (deprecated)
        :meth:`_finished`. Once True, it can never become False.
        """
        return self._event.is_set()

    @property
    def success(self):
        """
        Boolean indicating whether associated operation has completed.
        This is set to True at __init__ time or by calling
        :meth:`set_finished`, :meth:`set_exception`, or (deprecated)
        :meth:`_finished`. Once True, it can never become False.
        """
        return self.done and self._exception is None

    def _handle_failure(self):
        pass

    def _settled(self):
        """Hook for when status has completed and settled"""
        pass

    def _run_callbacks(self):
        """
        Set the Event and run the callbacks.
        """
        if self.timeout is None:
            timeout = None
        else:
            timeout = self.timeout + self.settle_time
        if not self._settled_event.wait(timeout):
            # We have timed out. It's possible that set_finished() has already
            # been called but we got here before the settle_time timer expired.
            # And it's possible that in this space be between the above
            # statement timing out grabbing the lock just below,
            # set_exception(exc) has been called. Both of these possibilties
            # are accounted for.
            self.log.warning("%r has timed out", self)
            with self._externally_initiated_completion_lock:
                # Set the exception and mark the Status as done, unless
                # set_exception(exc) was called externally before we grabbed
                # the lock.
                if self._exception is None:
                    exc = StatusTimeoutError(
                        f"Status {self!r} failed to complete in specified timeout."
                    )
                    self._exception = exc
        # Mark this as "settled".
        try:
            self._settled()
        except Exception:
            # No alternative but to log this. We can't supersede set_exception,
            # and we have to continue and run the callbacks.
            self.log.exception("%r encountered error during _settled()", self)
        # Now we know whether or not we have succeed or failed, either by
        # timeout above or by set_exception(exc), so we can set the Event that
        # will mark this Status as done.
        with self._lock:
            self._event.set()
        if self._exception is not None:
            try:
                self._handle_failure()
            except Exception:
                self.log.exception("%r encountered an error during _handle_failure()", self)
        # The callbacks have access to self, from which they can distinguish
        # success or failure.
        for cb in self._callbacks:
            try:
                cb(self)
            except Exception:
                self.log.exception(
                    "An error was raised on a background thread while "
                    "running the callback %r(%r).",
                    cb,
                    self,
                )
        self._callbacks.clear()

    def set_exception(self, exc):
        """
        Mark as finished but failed with the given Exception.
        This method should generally not be called by the *recipient* of this
        Status object, but only by the object that created and returned it.
        Parameters
        ----------
        exc: Exception
        """
        # Since we rely on this being raise-able later, check proactively to
        # avoid potentially very confusing failures.
        if not (
            isinstance(exc, Exception) or isinstance(exc, type) and issubclass(exc, Exception)
        ):
            # Note that Python allows `raise Exception` or raise Exception()`
            # so we allow a class or an instance here too.
            raise ValueError(f"Expected an Exception, got {exc!r}")

        # Ban certain Timeout subclasses that have special significance. This
        # would probably never come up except due to some rare user error, but
        # if it did it could be very confusing indeed!
        for exc_class in (StatusTimeoutError, WaitTimeoutError):
            if isinstance(exc, exc_class) or isinstance(exc, type) and issubclass(exc, exc_class):
                raise ValueError(
                    f"{exc_class} has special significance and cannot be set "
                    "as the exception. Use a plain TimeoutError or some other "
                    "subclass thereof."
                )

        with self._externally_initiated_completion_lock:
            if self._externally_initiated_completion:
                raise InvalidState(
                    "Either set_finished() or set_exception() has "
                    f"already been called on {self!r}"
                )
            self._externally_initiated_completion = True
            if isinstance(self._exception, StatusTimeoutError):
                # We have already timed out.
                return
            self._exception = exc
            self._settled_event.set()

    def set_finished(self):
        """
        Mark as finished successfully.
        This method should generally not be called by the *recipient* of this
        Status object, but only by the object that created and returned it.
        """
        with self._externally_initiated_completion_lock:
            if self._externally_initiated_completion:
                raise InvalidState(
                    "Either set_finished() or set_exception() has "
                    f"already been called on {self!r}"
                )
            self._externally_initiated_completion = True
        # Note that in either case, the callbacks themselves are run from the
        # same thread. This just sets an Event, either from this thread (the
        # one calling set_finished) or the thread created below.
        if self.settle_time > 0:
            threading.Timer(self.settle_time, self._settled_event.set).start()
        else:
            self._settled_event.set()

    def _finished(self, success=True, **kwargs):
        """
        Inform the status object that it is done and if it succeeded.
        This method is deprecated. Please use :meth:`set_finished` or
        :meth:`set_exception`.
        .. warning::
           kwargs are not used, but are accepted because pyepics gives
           in a bunch of kwargs that we don't care about.  This allows
           the status object to be handed directly to pyepics (but
           this is probably a bad idea for other reason.
           This may be deprecated in the future.
        Parameters
        ----------
        success : bool, optional
           if the action succeeded.
        """
        if success:
            self.set_finished()
        else:
            # success=False does not give any information about *why* it
            # failed, so set a generic exception.
            exc = UnknownStatusFailure(
                f"The status {self!r} has failed. To obtain more specific, "
                "helpful errors in the future, update the Device to use "
                "set_exception(...) instead of _finished(success=False)."
            )
            self.set_exception(exc)

    def exception(self, timeout=None):
        """
        Return the exception raised by the action.
        If the action has completed successfully, return ``None``. If it has
        finished in error, return the exception.
        Parameters
        ----------
        timeout: Union[Number, None], optional
            If None (default) wait indefinitely until the status finishes.
        Raises
        ------
        WaitTimeoutError
            If the status has not completed within ``timeout`` (starting from
            when this method was called, not from the beginning of the action).
        """
        if not self._event.wait(timeout=timeout):
            raise WaitTimeoutError("Status has not completed yet.")
        return self._exception

    def wait(self, timeout=None):
        """
        Block until the action completes.
        When the action has finished succesfully, return ``None``. If the
        action has failed, raise the exception.
        Parameters
        ----------
        timeout: Union[Number, None], optional
            If None (default) wait indefinitely until the status finishes.
        Raises
        ------
        WaitTimeoutError
            If the status has not completed within ``timeout`` (starting from
            when this method was called, not from the beginning of the action).
        StatusTimeoutError
            If the status has failed because the *timeout* that it was
            initialized with has expired.
        Exception
            This is ``status.exception()``, raised if the status has finished
            with an error.  This may include ``TimeoutError``, which
            indicates that the action itself raised ``TimeoutError``, distinct
            from ``WaitTimeoutError`` above.
        """
        if not self._event.wait(timeout=timeout):
            raise WaitTimeoutError("Status has not completed yet.")
        if self._exception is not None:
            raise self._exception

    @property
    def callbacks(self):
        """
        Callbacks to be run when the status is marked as finished
        """
        return self._callbacks

    @property
    def finished_cb(self):
        with self._lock:
            if len(self.callbacks) == 1:
                warn(
                    "The property `finished_cb` is deprecated, and must raise "
                    "an error if a status object has multiple callbacks. Use "
                    "the `callbacks` property instead.",
                    stacklevel=2,
                )
                (cb,) = self.callbacks
                assert cb is not None
                return cb
            else:
                raise UseNewProperty(
                    "The deprecated `finished_cb` property "
                    "cannot be used for status objects that have "
                    "multiple callbacks. Use the `callbacks` "
                    "property instead."
                )

    def add_callback(self, callback):
        """
        Register a callback to be called once when the Status finishes.
        The callback will be called exactly once. If the Status is finished
        before a callback is added, it will be called immediately. This is
        threadsafe.
        The callback will be called regardless of success of failure. The
        callback has access to this status object, so it can distinguish success
        or failure by inspecting the object.
        Parameters
        ----------
        callback: callable
            Expected signature: ``callback(status)``.
        """
        with self._lock:
            if self.done:
                # Call it once and do not hold a reference to it.
                callback(self)
            else:
                # Hold a strong reference to this. In other contexts we tend to
                # hold weak references to callbacks, but this is a single-shot
                # callback, so we will hold a strong reference until we call it,
                # and then clear this cache to drop the reference(s).
                self._callbacks.append(callback)

    @finished_cb.setter
    def finished_cb(self, cb):
        with self._lock:
            if not self.callbacks:
                warn(
                    "The setter `finished_cb` is deprecated, and must raise "
                    "an error if a status object already has one callback. Use "
                    "the `add_callback` method instead.",
                    stacklevel=2,
                )
                self.add_callback(cb)
            else:
                raise UseNewProperty(
                    "The deprecated `finished_cb` setter cannot "
                    "be used for status objects that already "
                    "have one callback. Use the `add_callbacks` "
                    "method instead."
                )

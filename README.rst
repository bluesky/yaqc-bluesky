=========
ophyd-yaq
=========

.. image:: https://img.shields.io/travis/bluesky/ophyd-yaq.svg
        :target: https://travis-ci.com/bluesky/ophyd-yaq

.. image:: https://img.shields.io/pypi/v/ophyd-yaq.svg
        :target: https://pypi.python.org/pypi/ophyd-yaq


An ophyd interface to the `yaq instrument control framework <https://yaq.fyi/>`_

To communicate with a yaq daemon, simply create an ophyd device::

    import ophyd_yaq
    device = ophyd_yaq.Device(port=39000)

Of course, you may also provide :code:`host` as an argument (default localhost).
You may also optionally provide :code:`name`, if you wish the ophyd device to have a different name than the yaq daemon.

:code:`ophyd_yaq` only exposes a subset of the functionality of yaq daemons.
Python users wishing to communicate with yaq may also be interested in `yaqc <https://python.yaq.fyi/yaqc/>`_.

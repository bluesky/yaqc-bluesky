============
yaqc-bluesky
============

.. image:: https://img.shields.io/travis/com/bluesky/yaqc-bluesky   :alt: Travis (.com)
        :target: https://travis-ci.com/bluesky/yaqc-bluesky

.. image:: https://img.shields.io/pypi/v/yaqc-bluesky.svg
        :target: https://pypi.python.org/pypi/yaqc-bluesky

.. image:: https://mybinder.org/badge.svg
	:target: https://mybinder.org/v2/gh/bluesky/yaqc-bluesky/master?urlpath=lab

An bluesky interface to the `yaq instrument control framework <https://yaq.fyi/>`_.

To communicate with a yaq daemon, simply create a device::

    import yaqc_bluesky
    device = yaqc_bluesky.Device(port=39000)

:code:`yaqc_bluesky` will read the traits from the daemon and return an appropriate device instance based on what it finds.
Of course, you may also provide :code:`host` as an argument (default localhost).
You may also optionally provide :code:`name`, if you wish the bluesky device to have a different name than the yaq daemon.

:code:`yaqc_bluesky` only exposes a subset of the functionality of yaq daemons.
Python users wishing to communicate with yaq may also be interested in `yaqc <https://python.yaq.fyi/yaqc/>`_.

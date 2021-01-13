# yaqc-bluesky

[![CI](https://img.shields.io/github/workflow/status/bluesky/yaqc-bluesky/python-test)](https://github.com/bluesky/yaqc-bluesky/actions?query=workflow%3Apython-test)
[![PyPI](https://img.shields.io/pypi/v/yaqc-bluesky)](https://pypi.org/project/yaqc-bluesky)
[![Conda](https://img.shields.io/conda/vn/conda-forge/yaqc-bluesky)](https://anaconda.org/conda-forge/yaqc-bluesky)
[![yaq](https://img.shields.io/badge/framework-yaq-orange)](https://yaq.fyi/)
[![black](https://img.shields.io/badge/code--style-black-black)](https://black.readthedocs.io/)
[![ver](https://img.shields.io/badge/calver-YYYY.M.MICRO-blue)](https://calver.org/)
[![log](https://img.shields.io/badge/change-log-informational)](https://gitlab.com/yaq/yaqc-bluesky/-/blob/master/CHANGELOG.md)

A bluesky interface to the [yaq instrument control framework](https://yaq.fyi/).

To communicate with a yaq daemon, simply create a device::

```python
import yaqc_bluesky
device = yaqc_bluesky.Device(port=39000)
```

`yaqc_bluesky` will read the traits from the daemon and return an appropriate device instance based on what it finds.
Of course, you may also provide `host` as an argument (default localhost).
You may also optionally provide `name`, if you wish the bluesky device to have a different name than the yaq daemon.

`yaqc_bluesky` only exposes a subset of the functionality of yaq daemons.
Python users wishing to communicate with yaq may also be interested in [yaqc](https://python.yaq.fyi/yaqc/).

You can play with yaq on bluesky using our binder:

[![binder]( https://mybinder.org/badge.svg)]( https://mybinder.org/v2/gh/bluesky/yaqc-bluesky/master?urlpath=lab)

## happi support

`yaqc_bluesky` provides support for [Happi](https://github.com/pcdshub/happi).
Read more about yaq and Happi at [python.yaq.fyi/happi](https://python.yaq.fyi/happi).


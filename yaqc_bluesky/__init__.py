# flake8: noqa

from ._device import *
from ._exceptions import *
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

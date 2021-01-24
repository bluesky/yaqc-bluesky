"""Support for happi -
pcdshub.github.io/happi
"""


import re
import copy

from happi.item import HappiItem, EntryInfo  # type: ignore


class YAQItem(HappiItem):
    name = EntryInfo(
        "Shorthand Python-valid name for the Python instance",
        optional=False,
        enforce=re.compile(r"^[^\d\W]\w*\Z"),
    )  # https://stackoverflow.com/a/10134719
    port = EntryInfo("TCP port.", enforce=int, optional=False)
    host = EntryInfo("Host.", optional=True, default="localhost")
    kwargs = copy.copy(HappiItem.kwargs)
    kwargs.default = {"port": "{{port}}", "host": "{{host}}", "name": "{{name}}"}
    device_class = EntryInfo(default="yaqc_bluesky.Device")

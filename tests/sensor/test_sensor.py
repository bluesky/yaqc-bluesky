import pathlib
import subprocess
import time
import math
import yaqc_bluesky
from yaqd_core import testing
from bluesky import RunEngine
from bluesky.plans import scan


config = pathlib.Path(__file__).parent / "config.toml"


@testing.run_daemon_entry_point("fake-spectrometer", config=config)
def test_describe_read():
    d = yaqc_bluesky.Device(39424)
    describe_keys = list(d.describe().keys())
    read_keys = list(d.read().keys())
    assert describe_keys == read_keys
    assert d.describe()["test_counts"]["shape"] == (551,)


@testing.run_daemon_entry_point("fake-spectrometer", config=config)
def test_hint_fields():
    d = yaqc_bluesky.Device(39424)
    fields = d.hints["fields"]
    for field in fields:
        assert field in d.describe().keys()
        assert field in d.read().keys()


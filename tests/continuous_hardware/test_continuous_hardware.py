import pathlib
import subprocess
import time
import math
import yaqc_bluesky
from yaqd_core import testing
from bluesky import RunEngine
from bluesky.plans import scan


config = pathlib.Path(__file__).parent / "config.toml"


@testing.run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_describe_read():
    d = yaqc_bluesky.Device(39424)
    d.set(0)
    describe_keys = list(d.describe().keys())
    read_keys = list(d.read().keys())
    assert describe_keys == read_keys


@testing.run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_hint_fields():
    d = yaqc_bluesky.Device(39424)
    fields = d.hints["fields"]
    for field in fields:
        assert field in d.describe().keys()
        assert field in d.read().keys()


@testing.run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_scan():
    d = yaqc_bluesky.Device(39424)
    RE = RunEngine({})
    RE(scan([], d, -1, 0.33, 10))
    assert math.isclose(d.read()[f"{d.name}_readback"]["value"], 0.33, abs_tol=1e-6)


@testing.run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_set():
    d = yaqc_bluesky.Device(39424)
    d.set(0)
    time.sleep(2)
    assert math.isclose(d.read()[f"{d.name}_readback"]["value"], 0)
    d.set(1)
    time.sleep(2)
    assert math.isclose(d.read()[f"{d.name}_readback"]["value"], 1, abs_tol=1e-6)


if __name__ == "__main__":
    test_scan()
    test_set()

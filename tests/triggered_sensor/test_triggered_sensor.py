import pathlib
import time
import subprocess
from yaqd_core import testing
import yaqc_bluesky


config = pathlib.Path(__file__).parent / "config.toml"


@testing.run_daemon_entry_point("fake-triggered-sensor", config=config)
def test_describe_read():
    d = yaqc_bluesky.Device(39425)
    d.trigger()
    describe_keys = list(d.describe().keys())
    read_keys = list(d.read().keys())
    assert describe_keys == read_keys


@testing.run_daemon_entry_point("fake-triggered-sensor", config=config)
def test_hint_fields():
    d = yaqc_bluesky.Device(39425)
    fields = d.hints["fields"]
    for field in fields:
        assert field in d.describe().keys()
        assert field in d.read().keys()


@testing.run_daemon_entry_point("fake-triggered-sensor", config=config)
def test_read():
    d = yaqc_bluesky.Device(39425)
    d.trigger()
    d._wait_until_still()
    assert -1 <= d.read()[f"{d.name}_random_walk"]["value"] <= 1


if __name__ == "__main__":
    test_describe_read()
    test_read()

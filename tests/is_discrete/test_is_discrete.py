import pathlib
import numpy as np
import time
import subprocess
from yaqd_core import testing
import yaqc_bluesky
import bluesky
from bluesky import plan_stubs as bps


config = pathlib.Path(__file__).parent / "config.toml"


@testing.run_daemon_entry_point("fake-discrete-hardware", config=config)
def test_identifier_is_in_read():
    d = yaqc_bluesky.Device(38383)
    read_keys = list(d.read().keys())
    assert f"{d.name}_position_identifier" in read_keys


@testing.run_daemon_entry_point("fake-discrete-hardware", config=config)
def test_identifier_is_in_describe():
    d = yaqc_bluesky.Device(38383)
    describe_keys = list(d.describe().keys())
    assert f"{d.name}_position_identifier" in describe_keys


@testing.run_daemon_entry_point("fake-discrete-hardware", config=config)
def test_describe_read():
    d = yaqc_bluesky.Device(38383)
    describe_keys = list(d.describe().keys())
    read_keys = list(d.read().keys())
    assert describe_keys == read_keys


@testing.run_daemon_entry_point("fake-discrete-hardware", config=config)
def test_hint_fields():
    d = yaqc_bluesky.Device(38383)
    fields = d.hints["fields"]
    for field in fields:
        assert field in d.describe().keys()
        assert field in d.read().keys()


@testing.run_daemon_entry_point("fake-discrete-hardware", config=config)
def test_set_read():
    d = yaqc_bluesky.Device(38383)
    d.set(470)
    time.sleep(1)
    out = d.read()
    assert out[f"{d.name}_position_identifier"]["value"] == "blue"
    d.set("green")
    time.sleep(1)
    out = d.read()
    assert np.isclose(out[d.name]["value"], 540.0)


@testing.run_daemon_entry_point("fake-discrete-hardware", config=config)
def test_mv():
    def plan():
        d = yaqc_bluesky.Device(38383)
        for identifier, position in d.yaq_client.get_position_identifiers().items():
            yield from bps.mv(d, identifier)
            assert np.isclose(d.read()[d.name]["value"], position)

    RE = bluesky.RunEngine()
    RE(plan())

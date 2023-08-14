import time
import happi
import pathlib
import appdirs
import yaqc_bluesky
from yaqd_core import testing
import numpy as np
import tempfile
import bluesky
from bluesky import plans as bsp


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-continuous-hardware", config=__here__ / "continuous-hardware-config.toml"
)
def test_property():
    device = yaqc_bluesky.Device(39424)
    device.set(0.222)
    time.sleep(1)
    assert np.isclose(device.position, 0.222)


@testing.run_daemon_entry_point(
    "fake-has-transformed-position", config=__here__ / "transformed-position-config.toml"
)
def test_count():
    RE = bluesky.RunEngine()
    d = yaqc_bluesky.Device(38999)
    RE(bsp.count([d.native_destination, d.native_position, d.native_reference_position], num=5))


@testing.run_daemon_entry_point(
    "fake-has-transformed-position", config=__here__ / "transformed-position-config.toml"
)
def test_scan():
    RE = bluesky.RunEngine()
    d = yaqc_bluesky.Device(38999)
    RE(
        bsp.scan(
            [d.native_destination, d.native_position, d.native_reference_position],
            d.native_destination,
            0,
            1,
            15,
        )
    )

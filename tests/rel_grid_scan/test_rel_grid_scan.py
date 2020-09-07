import pathlib
import time
import subprocess
import yaqc_bluesky
from yaqd_core import testing
from bluesky import RunEngine
from bluesky.plans import rel_grid_scan


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-triggered-sensor", config=__here__ / "triggered-sensor-config.toml"
)
@testing.run_daemon_entry_point(
    "fake-continuous-hardware", config=__here__ / "continuous-hardware-config.toml"
)
def test_simple_rel_grid_scan():
    RE = RunEngine()
    hardware = yaqc_bluesky.Device(39424)
    sensor = yaqc_bluesky.Device(39425)
    RE(rel_grid_scan([sensor], hardware, -1, 1, 15))


if __name__ == "__main__":
    test_simple_rel_grid_scan()

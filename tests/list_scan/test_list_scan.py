import pathlib
import time
import subprocess
import yaqc_bluesky
from yaqd_core import testing
from bluesky import RunEngine
from bluesky.plans import list_scan


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-triggered-sensor", config=__here__ / "triggered-sensor-config.toml"
)
@testing.run_daemon_entry_point(
    "fake-continuous-hardware", config=__here__ / "continuous-hardware-config.toml"
)
def test_simple_list_scan():
    RE = RunEngine()
    hardware = yaqc_bluesky.Device(39424)
    sensor = yaqc_bluesky.Device(39425)
    lis = [-10, -8, 4, 2, 10]
    RE(list_scan([sensor], hardware, lis))


if __name__ == "__main__":
    test_simple_list_scan()

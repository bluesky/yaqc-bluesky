import pathlib
import time
import subprocess
from cycler import cycler
import yaqc_bluesky
from yaqd_core import testing
from bluesky import RunEngine
from bluesky.plans import scan_nd


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-triggered-sensor", config=__here__ / "triggered-sensor-config.toml"
)
@testing.run_daemon_entry_point(
    "fake-continuous-hardware", config=__here__ / "continuous-hardware-config.toml"
)
def test_simple_scan_nd():
    RE = RunEngine()
    hardware1 = yaqc_bluesky.Device(39423)
    hardware2 = yaqc_bluesky.Device(39424)
    sensor = yaqc_bluesky.Device(39425)
    cy = cycler(hardware1, [1, 2, 3]) * cycler(hardware2, [4, 5, 6])
    RE(scan_nd([sensor], cy))


if __name__ == "__main__":
    test_simple_scan_nd()

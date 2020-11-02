import pathlib
import time
import subprocess
import yaqc_bluesky
from yaqd_core import testing
from bluesky import RunEngine
from bluesky.plans import count


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-triggered-sensor", config=__here__ / "triggered-sensor-config.toml"
)
def test_simple_count():
    RE = RunEngine()
    sensor = yaqc_bluesky.Device(39425)
    RE(count([sensor], 41))


if __name__ == "__main__":
    test_simple_count()

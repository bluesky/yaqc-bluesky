import pathlib
import time
import subprocess
from cycler import cycler
import yaqc_bluesky
from yaqd_core import testing
from bluesky import RunEngine
from bluesky.plans import rel_spiral_fermat


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-triggered-sensor", config=__here__ / "triggered-sensor-config.toml"
)
@testing.run_daemon_entry_point(
    "fake-continuous-hardware", config=__here__ / "continuous-hardware-config.toml"
)
def test_simple_rel_spiral_fermat():
    RE = RunEngine()
    hardware_x = yaqc_bluesky.Device(39423)
    hardware_y = yaqc_bluesky.Device(39424)
    sensor = yaqc_bluesky.Device(39425)
    RE(
        rel_spiral_fermat(
            [sensor],
            x_motor=hardware_x,
            y_motor=hardware_y,
            x_range=1,
            y_range=1,
            dr=0.5,
            factor=1,
        )
    )


if __name__ == "__main__":
    test_simple_rel_spiral_fermat()

import pathlib
import time
import subprocess
from cycler import cycler
import yaqc_bluesky
from yaqd_core import testing
from bluesky import RunEngine
from bluesky.plans import spiral_square


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-triggered-sensor", config=__here__ / "triggered-sensor-config.toml"
)
@testing.run_daemon_entry_point(
    "fake-continuous-hardware", config=__here__ / "continuous-hardware-config.toml"
)
def test_simple_spiral_square():
    RE = RunEngine()
    hardware_x = yaqc_bluesky.Device(39423)
    hardware_y = yaqc_bluesky.Device(39424)
    sensor = yaqc_bluesky.Device(39425)
    RE(
        spiral_square(
            [sensor],
            x_motor=hardware_x,
            y_motor=hardware_y,
            x_center=0,
            y_center=0,
            x_range=1,
            y_range=1,
            x_num=3,
            y_num=3,
        )
    )


if __name__ == "__main__":
    test_simple_spiral_square()

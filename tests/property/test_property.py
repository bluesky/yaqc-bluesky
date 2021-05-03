import time
import yaqc
import happi
import pathlib
import appdirs
import yaqc_bluesky
from yaqd_core import testing
import numpy as np
import tempfile


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-continuous-hardware", config=__here__ / "continuous-hardware-config.toml"
)
def test_property():
    device = yaqc_bluesky.Device(39424)
    device.set(0.222)
    time.sleep(1)
    assert np.isclose(device.position, 0.222)


if __name__ == "__main__":
    test_property()

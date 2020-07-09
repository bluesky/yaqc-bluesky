import pathlib
import subprocess
import time
import math
import ophyd_yaq
from bluesky import RunEngine
from bluesky.plans import scan


config = pathlib.Path(__file__).parent / "config.toml"


def run_daemon_entry_point(kind, config):
    def decorator(function):
        def wrapper():
            with subprocess.Popen([f"yaqd-{kind}", "--config", config]) as proc:
                tries = 100
                while True:
                    if tries <= 0:
                        break
                    try:
                        function()
                    except ConnectionError:
                        time.sleep(0.1)
                    else:
                        break
                    tries -= 1
                proc.terminate()
        return wrapper
    return decorator


@run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_set():
    d = ophyd_yaq.Device(39424)
    d.set(0)
    time.sleep(2)
    assert math.isclose(d.readback.get(), 0)
    d.set(1)
    time.sleep(2)
    assert math.isclose(d.readback.get(), 1)


@run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_scan():
    # for now, basically a smoke test
    d = ophyd_yaq.Device(39424)
    RE = RunEngine({})
    RE(scan([], d, -1, 1, 10))
    assert math.isclose(d.readback.get(), 1)


if __name__ == "__main__":
    test_set()
    test_scan()

import pathlib
import time
import subprocess
import yaqc_bluesky
from bluesky import RunEngine
from bluesky.plans import scan


__here__ = pathlib.Path(__file__).parent


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
                    except Exception:
                        proc.terminate()
                        raise
                    else:
                        break
                    tries -= 1
                proc.terminate()

        return wrapper

    return decorator


@run_daemon_entry_point(
    "fake-triggered-sensor", config=__here__ / "triggered-sensor-config.toml"
)
@run_daemon_entry_point(
    "fake-continuous-hardware", config=__here__ / "continuous-hardware-config.toml"
)
def test_simple_scan():
    RE = RunEngine()
    hardware = yaqc_bluesky.Device(39424)
    sensor = yaqc_bluesky.Device(39425)
    RE(scan([sensor], hardware, -10, 10, 15))


if __name__ == "__main__":
    test_simple_scan()

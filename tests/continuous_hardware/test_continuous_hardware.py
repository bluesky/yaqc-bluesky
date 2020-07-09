import pathlib
import subprocess
import time
import math
import ophyd_yaq


config = pathlib.Path(__file__).parent / "config.toml"


def run_daemon(kind, config):
    def decorator(function):
        def wrapper(kind=kind, config=config, function=function):
            with subprocess.Popen([f"yaqd-{kind}", "--config", config]) as proc:
                tries = 100
                while True:
                    if tries <= 0:
                        break
                    try:
                        function()
                    except ConnectionRefusedError:
                        time.sleep(0.1)
                    else:
                        break
                    tries -= 1
                proc.terminate()
        return wrapper
    return decorator


@run_daemon("fake-continuous-hardware", config=config)
def test_set():
    d = ophyd_yaq.Device(39424)
    d.set(0)
    time.sleep(2)
    assert math.isclose(d.readback.get(), 0)
    d.set(1)
    time.sleep(2)
    assert math.isclose(d.readback.get(), 1)


if __name__ == "__main__":
    test_set()

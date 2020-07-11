import pathlib
import time
import subprocess
import yaqc_bluesky


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
                    except Exception:
                        proc.terminate()
                        raise
                    else:
                        break
                    tries -= 1
                proc.terminate()

        return wrapper

    return decorator


@run_daemon_entry_point("fake-triggered-sensor", config=config)
def test_read():
    d = yaqc_bluesky.Device(39425)
    d.trigger()
    d._wait_until_still()
    assert -1 <= d.read()["random_walk"]["value"] <= 1


if __name__ == "__main__":
    test_read()

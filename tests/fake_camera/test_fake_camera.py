import pathlib
import time
import subprocess
from yaqd_core import testing
import yaqc_bluesky


config = pathlib.Path(__file__).parent / "config.toml"


@testing.run_daemon_entry_point("fake-camera", config=config)
def test_describe_read():
    d = yaqc_bluesky.Device(39426)
    d.trigger()
    describe_keys = list(d.describe().keys())
    read_keys = list(d.read().keys())
    assert describe_keys == read_keys
    assert "test_0" in d.describe()["test_image"]["dims"]
    assert "test_1" in d.describe()["test_image"]["dims"]
    assert "test_0" in d.describe()["test_y_index"]["dims"]
    assert "test_1" in d.describe()["test_x_index"]["dims"]


@testing.run_daemon_entry_point("fake-camera", config=config)
def test_hint_fields():
    d = yaqc_bluesky.Device(39426)
    fields = d.hints["fields"]
    for field in fields:
        assert field in d.describe().keys()
        assert field in d.read().keys()


if __name__ == "__main__":
    test_describe_read()
    test_hint_fields()

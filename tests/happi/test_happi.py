import yaqc
import happi
import pathlib
import appdirs
import yaqc_bluesky
from yaqd_core import testing
import tempfile


__here__ = pathlib.Path(__file__).parent


def test_add_then_find():
    item = yaqc_bluesky.happi_containers.YAQItem(name="test", port=38000)
    with tempfile.NamedTemporaryFile() as f:
        backend = happi.backends.backend(f.name)
        happi_client = happi.Client(database=backend)
        happi_client.add_device(item)
        output = happi_client.find_device(name="test")


@testing.run_daemon_entry_point(
    "fake-continuous-hardware", config=__here__ / "continuous-hardware-config.toml"
)
def test_add_then_load():
    item = yaqc_bluesky.happi_containers.YAQItem(name="test", port=39424)
    with tempfile.NamedTemporaryFile() as f:
        backend = happi.backends.backend(f.name)
        happi_client = happi.Client(database=backend)
        happi_client.add_device(item)
        output = happi_client.load_device(name="test")


if __name__ == "__main__":
    test_add_then_find()
    test_add_then_load()

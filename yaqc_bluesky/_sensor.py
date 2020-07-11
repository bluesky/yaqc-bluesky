from collections import OrderedDict

from ._base import Base
from ._status import Status


class Sensor(Base):

    def __init__(self, yaq_client, *, name=None):
        super().__init__(yaq_client, name=name)
        self._yaq_channel_names = self.yaq_client.get_channel_names()
        self._yaq_channel_units = self.yaq_client.get_channel_units()

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        measured = self.yaq_client.get_measured()  # locked by behavior of super().read
        for name in self._yaq_channel_names:
            out[name] = {"value": measured[name], "timestamp": ts}
        return out

    def trigger(self) -> Status:
        self.yaq_client.measure()
        return self._wait_until_still()

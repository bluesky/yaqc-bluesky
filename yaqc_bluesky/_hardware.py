from collections import OrderedDict

from ._base import Base


class Hardware(Base):

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        out["setpoint"] = {"value": self.yaq_client.get_destination(), "timestamp": ts}
        out["readback"] = {"value": self.yaq_client.get_position(), "timestamp": ts}
        return out

    def set(self, value):
        print(value)
        self.yaq_client.set_position(value)
        return self._wait_until_still()

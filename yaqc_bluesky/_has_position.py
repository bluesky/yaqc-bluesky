from collections import OrderedDict

from ._base import Base


class HasPosition(Base):
    def __init__(self, yaq_client, *, name=None):
        super().__init__(yaq_client, name=name)
        self.yaq_units = self.yaq_client.get_units()

    def _describe(self, out):
        out = super()._describe(out)
        meta = OrderedDict()
        meta["dtype"] = "number"
        meta["units"] = self.yaq_units
        out[f"{self.name}_setpoint"] = OrderedDict(self._field_metadata, **meta)
        out[f"{self.name}_readback"] = OrderedDict(self._field_metadata, **meta)
        return out

    @property
    def hints(self):
        out = super().hints
        out["fields"].append(f"{self.name}_readback")
        return out

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        out[f"{self.name}_setpoint"] = {
            "value": self.yaq_client.get_destination(),
            "timestamp": ts,
        }
        out[f"{self.name}_readback"] = {
            "value": self.yaq_client.get_position(),
            "timestamp": ts,
        }
        return out

    def set(self, value):
        self.yaq_client.set_position(value)
        return self._wait_until_still()

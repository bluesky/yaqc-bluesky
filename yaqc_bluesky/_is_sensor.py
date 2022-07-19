from collections import OrderedDict
import time

from ._base import Base


class IsSensor(Base):
    def __init__(self, yaq_client, *, name=None):
        super().__init__(yaq_client, name=name)
        self._yaq_channel_names = self.yaq_client.get_channel_names()
        self._yaq_channel_units = self.yaq_client.get_channel_units()
        self._yaq_channel_shapes = self.yaq_client.get_channel_shapes()

    def _describe(self, out):
        out = super()._describe(out)
        for name in self._yaq_channel_names:
            meta = OrderedDict()
            meta["shape"] = tuple(self._yaq_channel_shapes.get(name, ()))
            meta["dtype"] = "array" if meta["shape"] else "number"
            meta["units"] = self._yaq_channel_units.get(name)
            out[f"{self.name}_{name}"] = OrderedDict(self._field_metadata, **meta)
        return out

    @property
    def hints(self):
        out = super().hints
        out["fields"] += [f"{self.name}_{n}" for n in self._yaq_channel_names]
        return out

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        measured = self.yaq_client.get_measured()  # locked by behavior of super().read
        for name in self._yaq_channel_names:
            out[f"{self.name}_{name}"] = {"value": measured[name], "timestamp": ts}
        return out

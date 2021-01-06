from collections import OrderedDict

from ._base import Base


class IsSensor(Base):
    def __init__(self, yaq_client, *, name=None):
        super().__init__(yaq_client, name=name)
        self.trigger()  # need to run once to get channel information
        self._yaq_channel_names = self.yaq_client.get_channel_names()
        self._yaq_channel_units = self.yaq_client.get_channel_units()
        self._yaq_channel_shapes = {k: tuple() for k in self._yaq_channel_names}  # upstream broken

    def _describe(self, out):
        out = super()._describe(out)
        for name in self._yaq_channel_names:
            meta = OrderedDict()
            meta["dtype"] = "number"
            meta["units"] = self._yaq_channel_units[name]
            meta["shape"] = self._yaq_channel_shapes[name]
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

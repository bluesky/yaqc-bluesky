from collections import OrderedDict
import time
import numpy as np

from ._base import Base


class HasMapping(Base):
    def __init__(self, yaq_client, *, name=None):
        super().__init__(yaq_client, name=name)
        status = self.trigger()  # need to run once to get channel information
        while not status.done:
            time.sleep(0.01)
        self._yaq_channel_mappings = self.yaq_client.get_channel_mappings()
        self._yaq_mapping_units = self.yaq_client.get_mapping_units()
        self._yaq_mapping_shapes = {
            k: v.shape for k, v in self.yaq_client.get_mappings().items() if k != "mapping_id"
        }

    def _describe(self, out):
        out = super()._describe(out)
        map_dims = {}
        for name in self._yaq_mapping_shapes:
            meta = OrderedDict()
            meta["shape"] = tuple(i for i in self._yaq_mapping_shapes[name] if i != 1)
            meta["dtype"] = "array" if meta["shape"] else "number"
            meta["units"] = self._yaq_mapping_units.get(name)
            meta["dims"] = [
                f"{self.name}_{i}" for i, v in enumerate(self._yaq_mapping_shapes[name]) if v > 1
            ]
            meta["independent"] = True
            map_dims[name] = set(meta["dims"])
            out[f"{self.name}_{name}"] = OrderedDict(self._field_metadata, **meta)

        for chan, dims in self._yaq_channel_mappings.items():
            ch_dims = set()
            for d in dims:
                ch_dims.update(map_dims[d])
            out[f"{self.name}_{chan}"]["dims"] = sorted(ch_dims)
        return out

    @property
    def hints(self):
        out = super().hints
        out["fields"] += [f"{self.name}_{n}" for n in self._yaq_mapping_shapes]
        return out

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        measured = self.yaq_client.get_mappings()  # locked by behavior of super().read
        for name in measured:
            if name == "mapping_id":
                continue
            out[f"{self.name}_{name}"] = {"value": np.squeeze(measured[name]), "timestamp": ts}
        return out

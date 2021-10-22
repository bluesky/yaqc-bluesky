from collections import OrderedDict

from ._base import Base


class HasPosition(Base):
    def __init__(self, yaq_client, *, name=None):
        super().__init__(yaq_client, name=name)
        self.yaq_units = self.yaq_client.get_units()

    def _describe(self, out):
        out = super()._describe(out)
        out[self.name] = out[f"{self.name}_position"]
        out.move_to_end(self.name, last=False)
        del out[f"{self.name}_position"]
        return out

    @property
    def hints(self):
        out = super().hints
        out["fields"].append(f"{self.name}")
        return out

    @property
    def position(self) -> float:
        return self.yaq_client.get_position()

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        out[self.name] = out[f"{self.name}_position"]
        out.move_to_end(self.name, last=False)
        del out[f"{self.name}_position"]
        return out

    def set(self, value):
        self.yaq_client.set_position(value)
        return self._wait_until_still()

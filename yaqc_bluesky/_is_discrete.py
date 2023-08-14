from collections import OrderedDict
import time
import warnings

from ._has_position import HasPosition


class IsDiscrete(HasPosition):

    def _describe(self, out):
        out = super()._describe(out)
        meta = OrderedDict()
        meta["shape"] = []
        meta["dtype"] = "string"
        out[f"{self.name}_identifier"] = meta
        return out

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        identifier = dict()
        identifier["value"] = self.yaq_client.get_identifier()
        identifier["timestamp"] = ts
        out[f"{self.name}_identifier"] = identifier
        return out

    def set(self, value):
        try:
            self.yaq_client.set_position(value)
        except TypeError:
            self.yaq_client.set_identifier(value)
        return self._wait_until_still()

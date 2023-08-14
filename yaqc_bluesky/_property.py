__all__ = ["PropertyDevice"]


import types
import time

import yaqc  # type: ignore

from ._status import Status


class PropertyDevice(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self._yaq_property = self.parent.yaq_client.properties[self.name]
        if self._yaq_property.type in ["int", "float", "double"]:
            self._dtype = "number"
        elif self._yaq_property.type == "string":
            self._dtype = "string"
        else:
            self._dtype = "array"

        self._setpoint = float("nan")

        def set(self, value) -> Status:
            self._setpoint = float(value)
            self._yaq_property(value)
            st = Status()
            st.set_finished()
            st.wait()
            return st

        if self._yaq_property._property["setter"]:
            setattr(self, "set", types.MethodType(set, self))

    def describe(self) -> dict:
        out = dict()
        out[f"{self.parent.name}_{self.name}_readback"] = {"dtype": self._dtype, "shape": [], "source": f"yaq:{self.parent.yaq_name}"
}
        if self._yaq_property._property["getter"]:
            out[f"{self.parent.name}_{self.name}_setpoint"] = {"dtype": self._dtype, "shape": [], "source": f"yaq:{self.parent.yaq_name}"}
        return out

    def read(self) -> dict:
        ts = time.time()
        out = dict()
        out[f"{self.parent.name}_{self.name}_readback"] = {"value": self._yaq_property(), "timestamp": ts}
        if self._yaq_property._property["getter"]:
            out[f"{self.parent.name}_{self.name}_setpoint"] = {"value": self._setpoint, "timestamp": ts}
        return out

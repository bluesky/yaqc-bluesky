__all__ = ["Base"]


from collections import OrderedDict
import threading
import time
from typing import Dict

from ._callbacks import with_func_callbacks
from ._status import Status


class Base:

    @with_func_callbacks
    def __init__(self, yaq_client, *, name=None):
        self.yaq_client = yaq_client
        self.yaq_traits = yaq_client.traits
        self.yaq_name = self.yaq_client.id()["name"]
        if name is None:
            self.name = self.yaq_name
        else:
            self.name = name
        self.parent = None
        self._lock = threading.Lock()

    def __repr__(self):
        name = self.yaq_name
        protocol = self.yaq_client._protocol["protocol"]
        host = self.yaq_client._host
        port = self.yaq_client._port
        return f"<yaqc_bluesky.Device to {host}:{port} ({protocol}:{name})>"

    @with_func_callbacks
    def _describe(self, out):
        for key, prop in self.yaq_client.properties.items():
            if not prop.dynamic or prop.record_kind != "data":
                continue
            out[f"{self.name}_{key}"] = self._field_metadata
            if prop.type in ["int", "float", "double"]:
                out[f"{self.name}_{key}"]["dtype"] = "number"
            elif prop.type == "string":
                out[f"{self.name}_{key}"]["dtype"] = "string"
            else:
                out[f"{self.name}_{key}"]["dtype"] = "array"
                # TODO shape?
            if hasattr(prop, "units"):
                out[f"{self.name}_{key}"]["units"] = prop.units()
            if hasattr(prop, "limits"):
                lo, hi = prop.limits()
                out[f"{self.name}_{key}"]["lower_ctrl_limit"] = lo
                out[f"{self.name}_{key}"]["upper_ctrl_limit"] = hi

        return out

    @with_func_callbacks
    def describe(self) -> OrderedDict:
        out: OrderedDict = OrderedDict()
        out = self._describe(out)
        return out

    @with_func_callbacks
    def describe_configuration(self) -> OrderedDict:
        out: OrderedDict = OrderedDict()
        for key, prop in self.yaq_client.properties.items():
            if prop.record_kind != "metadata":
                continue
            out[f"{self.name}_{key}"] = self._field_metadata
            if prop.type in ["int", "float", "double"]:
                out[f"{self.name}_{key}"]["dtype"] = "number"
            elif prop.type == "string":
                out[f"{self.name}_{key}"]["dtype"] = "string"
            else:
                out[f"{self.name}_{key}"]["dtype"] = "array"
                # TODO shape?
            if hasattr(prop, "units"):
                out[f"{self.name}_{key}"]["units"] = prop.units()
            if hasattr(prop, "limits"):
                lo, hi = prop.limits()
                out[f"{self.name}_{key}"]["lower_ctrl_limit"] = lo
                out[f"{self.name}_{key}"]["upper_ctrl_limit"] = hi

        return out

    @property
    def _field_metadata(self) -> OrderedDict:
        """Metadata to be shared by all fields for this daemon."""
        out: OrderedDict = OrderedDict()
        out["source"] = f"yaq:{self.yaq_name}"
        out["yaq_port"] = self.yaq_client._port
        out["yaq_host"] = self.yaq_client._host
        out["shape"] = tuple()  # should be None, but upstream bluesky is broken
        return out

    @property
    def hints(self) -> Dict:
        out: Dict = {}
        out["fields"] = []
        return out

    @with_func_callbacks
    def _read(self, out, ts) -> OrderedDict:
        for key, prop in self.yaq_client.properties.items():
            if not prop.dynamic or prop.record_kind != "data":
                continue
            out[f"{self.name}_{key}"] = {
                "value": prop(),
                "timestamp": ts,
            }
        return out

    @with_func_callbacks
    def read(self) -> OrderedDict:
        with self._lock:
            out: OrderedDict = OrderedDict()
            ts = time.time()
            out = self._read(out, ts)
        return out

    @with_func_callbacks
    def read_configuration(self) -> OrderedDict:
        out = OrderedDict()
        ts = time.time()
        for key, prop in self.yaq_client.properties.items():
            if prop.record_kind != "metadata":
                continue
            out[f"{self.name}_{key}"] = {
                "value": prop(),
                "timestamp": ts,
            }
        return out

    @with_func_callbacks
    def trigger(self) -> Status:
        # should be overloaded for those devices that need a trigger
        st = Status()
        st._finished()
        return st

    @with_func_callbacks
    def _wait_until_still(self):
        st = Status()

        def poll():
            exc_count = 0
            sleep = 0.01
            while True:
                try:
                    if self.yaq_client.busy():
                        time.sleep(sleep)
                        # exponential backoff
                        sleep = min(0.1, sleep * 2)
                    else:
                        break
                except Exception as e:
                    exc_count += 1
                    if exc_count > 10:
                        st.set_exception(e)
                        return
                    time.sleep(0.1)
            st.set_finished()

        threading.Thread(target=poll).start()
        return st

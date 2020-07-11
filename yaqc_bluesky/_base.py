__all__ = ["Base"]


from collections import OrderedDict
import threading
import time

from ._status import Status


class Base:

    def __init__(self, yaq_client, *, name=None):
        self.yaq_client = yaq_client
        self.yaq_traits = yaq_client.traits
        if name is None:
            self.name = self.yaq_client.id()["name"]
        else:
            self.name = name
        self.parent = None
        self.hints = {}
        self._lock = threading.Lock()

    def trigger(self) -> Status:
        # should be overloaded for those devices that need a trigger
        st = Status()
        st._finished()
        return st

    def _read(self, out, ts) -> OrderedDict:
        out["busy"] = {"value": self.yaq_client.busy(), "timestamp": ts}
        return out

    def read(self) -> OrderedDict:
        with self._lock:
            out = OrderedDict()
            ts = time.time()
            out = self._read(out, ts)
        return out

    def read_configuration(self) -> OrderedDict:
        return OrderedDict()

    def set(self, position) -> Status:
        raise NotImplementedError

    def describe(self) -> OrderedDict:
        out = OrderedDict()
        out["position"] = {'source': 'XF23-ID:SOME_PV_NAME',
                           'dtype': 'number',
                           'shape': []}
        return out

    def describe_configuration(self) -> OrderedDict:
        return OrderedDict()

    def _wait_until_still(self):
        st = Status()
        def poll():
            while True:
                r = self.read()
                if r["busy"]["value"]:
                    time.sleep(0.1)
                else:
                    break
            st._finished()
        threading.Thread(target=poll).start()
        return st

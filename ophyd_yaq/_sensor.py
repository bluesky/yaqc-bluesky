import threading
from collections import OrderedDict
import time
from typing import Dict, List

from ._base import Base


class Sensor(Base):
    busy = Cpt(Signal, kind="omitted")

    def __init__(self, yaq_client, name):
        # create a signal for each channel
        self.yaq_client = yaq_client
        self._yaq_channel_names: List[str] = yaq_client.get_channel_names()
        self._yaq_channel_units: Dict[str, str] = yaq_client.get_channel_units()
        self._busy_lock = threading.Lock()
        super().__init__()

    def describe(self):
        out = OrderedDict()
        for name in self._yaq_channel_names:
            out[name] = {"units" : self._yaq_channel_units[name]}
        return out

    def read(self):
        out = OrderedDict()
        measured = self.yaq_client.get_measured()
        ts = time.time()
        for k, v in measured:
            out[k] = {"value" : v, "timestamp" : ts}

    def trigger(self):
        with self._busy_lock:
            self.busy.put(1)
        self.yaq_client.measure()
        st = DeviceStatus(self)

        def poll_busy():
            while True:
                self._read_yaq()
                if self.yaq_client.busy():
                    time.sleep(0.1)
                else:
                    break
            with self._busy_lock:
                self.busy.put(False)
            st._finished()

        threading.Thread(target=poll_busy).start()
        # update the signals
        return st

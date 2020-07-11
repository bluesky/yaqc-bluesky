from collections import OrderedDict
import threading
import time

from ._base import Base
from ._status import Status


class Hardware(Base):

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        out["setpoint"] = {"value" : self.yaq_client.get_destination(), "timestamp" : ts}
        out["readback"] = {"value" : self.yaq_client.get_position(), "timestamp" : ts}
        return out

    def set(self, value):
        print(value)
        self.yaq_client.set_position(value)
        st = Status()

        def poll_busy():
            while True:
                r = self.read()
                if r["busy"]["value"]:
                    time.sleep(0.1)
                else:
                    break
            st._finished()

        threading.Thread(target=poll_busy).start()
        return st

from ophyd import Component as Cpt, Signal, DeviceStatus
import threading
import time

from ._base import Base


class Hardware(Base):
    setpoint = Cpt(Signal, kind="hinted")
    readback = Cpt(Signal)

    def set(self, value):
        with self._busy_lock:
            self.busy.put(1)
        self.yaq_client.set_position(value)
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

    def _read_yaq(self):
        self.setpoint.put(self.yaq_client.get_destination())
        self.readback.put(self.yaq_client.get_position())
        b = self.yaq_client.busy()
        with self._busy_lock:
            self.busy.put(int(b))

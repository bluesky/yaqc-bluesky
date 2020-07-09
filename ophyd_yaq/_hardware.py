from ophyd import Device, Component as Cpt, Signal, DeviceStatus
import yaqc
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
            busy = self.yaq_client.busy()
            while busy:
                time.sleep(.1)
                busy = self.yaq_client.busy()
            with self._busy_lock:
                self.busy.put(int(busy))
            st._finished()

        threading.Thread(target=poll_busy).start()
        # update the signals
        self._read_yaq()
        return st

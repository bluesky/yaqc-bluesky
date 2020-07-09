from ophyd import Device, Component as Cpt, Signal, DeviceStatus
import yaqc
import threading
import time


class Base(Device):
    busy = Cpt(Signal, kind="omitted")

    def __init__(self, yaq_client, name):
        self.yaq_client = yaq_client
        self.yaq_traits = yaq_client.traits
        self._busy_lock = threading.Lock()
        if name is None:
            name = self.yaq_client.id()["name"]
        super().__init__(name=name)

    def _read_yaq(self):
        self.setpoint.put(self.yaq_client.get_destination())
        self.readback.put(self.yaq_client.get_position())
        b = self.yaq_client.busy()
        with self._busy_lock:
            self.busy.put(int(b))

    def read(self):
        self._read_yaq()
        return super().read()

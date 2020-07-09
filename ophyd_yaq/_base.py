from ophyd import Device, Component as Cpt, Signal
import threading


class Base(Device):
    busy = Cpt(Signal, kind="omitted")

    def __init__(self, yaq_client, name):
        self.yaq_client = yaq_client
        self.yaq_traits = yaq_client.traits
        self._busy_lock = threading.Lock()
        if name is None:
            name = self.yaq_client.id()["name"]
        super().__init__(name=name)

    def read(self):
        self._read_yaq()
        return super().read()

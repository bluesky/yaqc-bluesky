from ophyd import Device, Component as Cpt, Signal, DeviceStatus
import yaqc
import threading
import time


class YaqMotor(Device):
    setpoint = Cpt(Signal, kind="hinted")
    readback = Cpt(Signal)
    busy = Cpt(Signal, kind="omitted")

    def __init__(self, port, *, name=None):
        self._client = yaqc.Client(port)
        assert 'has-position' in self._client.traits
        self._busy_lock = threading.Lock()
        if name is None:
            name = self._client.id()["name"]
        super().__init__(name=name)
        # force initial reading
        self._read_yaq()

    def set(self, value):
        with self._busy_lock:
            self.busy.put(1)
        self._client.set_position(value)
        st = DeviceStatus(self)

        def poll_busy():
            busy = self._client.busy()
            while busy:
                time.sleep(.1)
                busy = self._client.busy()
            with self._busy_lock:
                self.busy.put(int(busy))
            st._finished()

        threading.Thread(target=poll_busy).start()
        # update the signals
        self._read_yaq()
        return st

    def _read_yaq(self):
        self.setpoint.put(self._client.get_destination())
        self.readback.put(self._client.get_position())
        b = self._client.busy()
        with self._busy_lock:
            self.busy.put(int(b))

    def read(self):
        self._read_yaq()
        return super().read()

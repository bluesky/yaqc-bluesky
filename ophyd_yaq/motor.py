from ophyd import Device, Component as Cpt, Signal, DeviceStatus
import yaqc
import threading
import time

class YaqMotor(Device):
    setpoint = Cpt(Signal, kind="hinted")
    readback = Cpt(Signal)
    busy = Cpt(Signal, kind="omitted")

    def __init__(self, port, *, name):
        self._client = yaqc.Client(port)
        assert 'has-position' in self._client.send('get_traits')
        self._busy_lock = threading.Lock()
        super().__init__(name=name)
        # force initial reading
        self._read_yaq()

    def set(self, value):
        with self._busy_lock:
            self.busy.put(1)
        self._client.send("set_position", value)
        st = DeviceStatus(self)

        def poll_busy():
            busy = self._client.send('busy')
            while busy:
                time.sleep(.1)
                busy = self._client.send('busy')
            with self._busy_lock:
                self.busy.put(int(busy))
            st._finished()

        threading.Thread(target=poll_busy).start()
        # update the signals
        self._read_yaq()
        return st

    def _read_yaq(self):
        v = self._client.send("get_state")
        self.setpoint.put(v["destination"])
        self.readback.put(v["position"])
        b = self._client.send('busy')
        with self._busy_lock:
            self.busy.put(int(b))

    def read(self):
        self._read_yaq()
        return super().read()

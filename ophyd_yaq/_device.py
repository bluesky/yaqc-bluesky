__all__ = ["Device"]


import yaqc

from ._base import Base
from ._hardware import Hardware
from ._sensor import Sensor


def Device(port, *, host="127.0.0.1", name=None):
    c = yaqc.Client(port=port, host=host)
    clss = []
    if "has-position" in c.traits:
        clss.append(Hardware)
    if "is-sensor" in c.traits:
        clss.append(Sensor)
    cls = type("YaqDevice", tuple(clss), {})
    obj = cls(yaq_client=c, name=name)
    print(obj.setpoint)
    obj._read_yaq()  # force initial reading to get things started
    return obj

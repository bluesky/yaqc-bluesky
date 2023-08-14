__all__ = ["Device"]


import yaqc  # type: ignore

from ._has_position import HasPosition
from ._is_sensor import IsSensor
from ._has_measure_trigger import HasMeasureTrigger
from ._has_mapping import HasMapping
from ._has_dependent import HasDependent
from ._is_discrete import IsDiscrete


traits = [  # MRO goes from top to bottom
    ("is-discrete", IsDiscrete),
    ("has-position", HasPosition),
    ("has-measure-trigger", HasMeasureTrigger),
    ("has-mapping", HasMapping),
    ("is-sensor", IsSensor),
]


def Device(port, *, host="127.0.0.1", name=None):
    c = yaqc.Client(port=port, host=host)
    # collect classes
    clss = []
    for trait, cls in traits:
        if trait in c.traits:
            clss.append(cls)
    # Special case for now, should likely become a proper trait
    if hasattr(c, "get_dependent_hardware"):
        clss.append(HasDependent)
    # make instance
    cls = type("YAQDevice", tuple(clss), {})
    obj = cls(yaq_client=c, name=name)
    status = obj.trigger()  # force initial reading to get things started
    while not status.done:
        pass
    obj.read()  # force initial reading to get things started
    return obj

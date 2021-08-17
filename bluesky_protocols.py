"""This file only intended for static type-checking."""


from yaqc_bluesky._base import Base
from yaqc_bluesky._has_position import HasPosition
from yaqc_bluesky._status import Status
from bluesky import protocols as bluesky_protocols


a: bluesky_protocols.Readable = Base(0)
b: bluesky_protocols.Movable = HasPosition(0)
c: bluesky_protocols.Status = Status()

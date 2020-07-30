from ._status import Status
from ._base import Base


class HasMeasureTrigger(Base):
    def trigger(self) -> Status:
        self.yaq_client.measure()
        return self._wait_until_still()

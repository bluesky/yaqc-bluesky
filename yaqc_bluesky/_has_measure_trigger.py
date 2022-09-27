from ._status import Status
from ._base import Base
from ._callbacks import with_func_callbacks


class HasMeasureTrigger(Base):

    @with_func_callbacks
    def trigger(self) -> Status:
        self.yaq_client.measure()
        return self._wait_until_still()

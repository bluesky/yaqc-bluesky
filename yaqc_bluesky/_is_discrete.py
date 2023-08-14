from collections import OrderedDict
import time
import warnings

from ._has_position import HasPosition


class IsDiscrete(HasPosition):

    def set(self, value):
        try:
            self.yaq_client.set_position(value)
        except TypeError:
            self.yaq_client.set_identifier(value)
        return self._wait_until_still()

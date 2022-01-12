from collections import OrderedDict
import time
import warnings

from ._base import Base


class HasDependent(Base):
    def __init__(self, yaq_client, *, name=None):
        super().__init__(yaq_client, name=name)
        # Avoid circular import
        from ._device import Device

        self._dependent_hardware = {}
        for k, v in self.yaq_client.get_dependent_hardware().items():
            try:
                host, port = v.split(":", 1)
                # replace hosts local to my own daemon, which may be remote to the client
                if host in ("localhost", "127.0.0.1"):
                    host = self.yaq_client._host
                self._dependent_hardware[k] = Device(port=port, host=host)
            except ConnectionError as e:
                warnings.warn(
                    f"Unable to connect to {k} from {self.name}, ignoring dependent relationship."
                )

    def _describe(self, out):
        out = super()._describe(out)
        for d in self._dependent_hardware.values():
            out.update(d.describe())
        return out

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        for d in self._dependent_hardware.values():
            out.update(d.read())
        return out

    def read_configuration(self) -> OrderedDict:
        out = super().read_configuration()
        for d in self._dependent_hardware.values():
            out.update(d.read_configuration())
        return out

    def describe_configuration(self) -> OrderedDict:
        out = super().describe_configuration()
        for d in self._dependent_hardware.values():
            out.update(d.describe_configuration())
        return out

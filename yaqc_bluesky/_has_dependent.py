from collections import OrderedDict
import time
import warnings

from ._base import Base


class HasDependent(Base):
    def __init__(self, yaq_client, *, name=None):
        super().__init__(yaq_client, name=name)
        # Avoid circular import
        from ._device import Device

        self.prefix = f"{self.name}_"
        self._dependent_hardware = {
            k[len(self.prefix) :] if k.startswith(self.prefix) else k: v
            for k, v in self.yaq_client.get_dependent_hardware().items()
        }

        for k, v in self._dependent_hardware.items():
            try:
                host, port = v.split(":", 1)
                # replace hosts local to my own daemon, which may be remote to the client
                if host in ("localhost", "127.0.0.1"):
                    host = self.yaq_client._host
                setattr(self, k, Device(port=int(port), host=host))
                getattr(self, k).parent = self
            except (ConnectionError, OSError) as e:
                warnings.warn(
                    f"Unable to connect to {k} from {self.name}, ignoring dependent relationship."
                )

    def _describe(self, out):
        out = super()._describe(out)
        for d in self._dependent_hardware.keys():
            if not hasattr(self, d):
                continue
            d = getattr(self, d)
            out.update(
                {
                    k if k.startswith(self.prefix) else f"{self.name}_{k}": v
                    for k, v in d.describe().items()
                }
            )
        return out

    def _read(self, out, ts) -> OrderedDict:
        out = super()._read(out, ts)
        for d in self._dependent_hardware.keys():
            if not hasattr(self, d):
                continue
            d = getattr(self, d)
            out.update(
                {
                    k if k.startswith(self.prefix) else f"{self.name}_{k}": v
                    for k, v in d.read().items()
                }
            )
        return out

    def read_configuration(self) -> OrderedDict:
        out = super().read_configuration()
        for d in self._dependent_hardware.keys():
            if not hasattr(self, d):
                continue
            d = getattr(self, d)
            out.update(
                {
                    k if k.startswith(self.prefix) else f"{self.name}_{k}": v
                    for k, v in d.read_configuration().items()
                }
            )
        return out

    def describe_configuration(self) -> OrderedDict:
        out = super().describe_configuration()
        for d in self._dependent_hardware.keys():
            if not hasattr(self, d):
                continue
            d = getattr(self, d)
            out.update(
                {
                    k if k.startswith(self.prefix) else f"{self.name}_{k}": v
                    for k, v in d.describe_configuration().items()
                }
            )
        return out

    @property
    def component_names(self):
        return tuple(self._dependent_hardware.keys())

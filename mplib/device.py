"""
Device ORM to pull the various config sources.
"""

from .config import GeneralConfig, LayoutConfig


class Device:
    # pylint: disable=missing-docstring
    __slots__ = "client_id", "device_id", "v6_path", "_general", "_layout"

    def __init__(self, client_id: int, device_id: str, v6_path: str = None):
        self.client_id = client_id
        self.device_id = device_id
        self.v6_path = v6_path
        self._general = None
        self._layout = None

    @property
    def general(self) -> GeneralConfig:
        if self._general is None:
            self._general = GeneralConfig.from_v6_id(self.client_id,
                                                     self.device_id,
                                                     self.v6_path)
        return self._general

    @property
    def layout(self) -> LayoutConfig:
        if self._layout is None:
            self._layout = LayoutConfig.from_v6_id(self.client_id,
                                                   self.device_id,
                                                   self.v6_path)
        return self._layout

"""
Layout and Display app.
"""
from .section import Config, ConfigSection


class LayoutSection(ConfigSection):
    """Zone container for the LayoutConfig"""
    __slots__ = ["x1", "y1", "x2", "y2", "apps"]

    @staticmethod
    def from_v6_values(data):
        # pylint: disable=invalid-name
        return {
            "x1": data["AREA"]["X1"],
            "y1": data["AREA"]["Y1"],
            "x2": data["AREA"]["X2"],
            "y2": data["AREA"]["Y2"],
            "apps": data["APPS"],
        }

    def to_v6_values(self):
        return {
            "AREA": {
                "X1": self.x1,
                "Y1": self.y1,
                "X2": self.x2,
                "Y2": self.y2,
            },
            "APPS": self.apps
        }

    @classmethod
    def from_v6_layout(cls, data):
        """Create a """
        data = cls.from_v6_values(data)
        return cls(**data)

    def __init__(self, x1, y1, x2, y2, apps):
        # pylint: disable=invalid-name,too-many-arguments
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.apps = apps


class LayoutConfig(Config):
    """
    Store information about what apps should be run, in which order, in which
    sectons, orientation information, and whether or not the scroller and
    minizone should be displayed.
    """
    __slots__ = "vertical", "layout", "scroller", "minizone", "zones"
    file_path = "/home/mediapanel/themes/layout.json"

    @staticmethod
    def from_v6_values(data):
        return {
            # Whether the device should use vertical or horizontal layout
            "vertical": data["SETTINGS"]["VERTICAL"],

            # Number of layout, useful only for UI, not on device
            "layout": data["SETTINGS"]["LAYOUT"],

            # Whether or not the scroller should be displayed
            "scroller": data["SETTINGS"]["SCROLLER"],

            # Whether or not the minizone should be displayed (on the scroller)
            "minizone": data["SETTINGS"]["MINIZONE"],

            # Information about each of the full zones
            "zones": [LayoutSection.from_v6_layout(zone)
                      for zone in data["ZONES"]]
        }

    def to_v6_values(self):
        return {
            "SETTINGS": {
                "VERTICAL": self.vertical,
                "LAYOUT": self.layout,
                "SCROLLER": self.scroller,
                "MINIZONE": self.minizone
            },
            "ZONES": [x.to_v6_values() for x in self.zones]
        }

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.vertical = data["vertical"]
        self.layout = data["layout"]
        self.scroller = data["scroller"]
        self.minizone = data["minizone"]
        self.zones = data["zones"]

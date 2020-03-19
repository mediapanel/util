"""
General device configuration.
"""
from .section import Config


class GeneralConfig(Config):
    """
    Store information about the device that might not be relevant to a
    particular application or might not be useful to the device itself.
    """

    # pylint: disable=too-many-instance-attributes

    __slots__ = ["nickname", "logo_interval", "timezone",
                 "address", "city", "state", "zipcode", "country",
                 "filter_content", "weather_alerts", "moderated"]
    file_path = "home/mediapanel/themes/generalConfig.json"

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        # The nickname given to the device, as shown on the website and on
        # the "Show Device Nickname" prompt
        # ::TODO:: this is mirrored in SQL correctly, right?
        self.nickname = config["nickname"]

        # ::TODO:: AFAIK unused?
        self.logo_interval = config["logo_interval"]

        # Address and time information for the device
        self.timezone = config["timezone"]
        self.address = config["address"]
        self.city = config["city"]
        self.state = config["state"]
        self.zipcode = config["zipcode"]
        self.country = config["country"]

        # Use the bad-word filter on prepared dynamic text
        self.filter_content = config["filter_content"]

        # Show weather alerts
        # ::TODO:: check if this is used
        self.weather_alerts = config["weather_alerts"]

    @staticmethod
    def from_v6_values(data):
        data = {x.lower(): y for x, y in data.items()}
        data["nickname"] = data["devicenickname"]
        data["logo_interval"] = data["logointerval"]
        data["filter_content"] = data["filtercontent"]
        return data

    def to_v6_values(self):
        return {
            "DEVICENICKNAME": self.nickname,
            "LOGOINTERVAL": self.logo_interval,
            "TIMEZONE": self.timezone,
            "ADDRESS": self.address,
            "CITY": self.city,
            "STATE": self.state,
            "ZIPCODE": self.zipcode,
            "COUNTRY": self.country,
            "FILTERCONTENT": self.filter_content,
            "WEATHER_ALERTS": self.weather_alerts,
            # ::TODO:: are these used?
            "WOEID": "",
            "WIFINAME": "",
            "MODERATED": False,
            "USEWIFI": False
        }

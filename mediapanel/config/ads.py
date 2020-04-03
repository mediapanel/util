"""
Ads device configuration
"""

from enum import Enum, auto
from datetime import datetime
from typing import List, Tuple

from .section import Config


class Ad:
    __slots__ = [
        # Scheduling
        "timeframe",  # Timeframe object
        "playtime",  # If not 0, amount of time an ad should play for
                     # Listed as RUNTIMEAUTO and RUNTIMEINTERVAL in v6 code

        # Media
        "background",  # Media displayed in background
        "media",  # Media to be displayed front and center

        # Textual display
        "lines",  # Lines to be displayed alongside media - if any
        "title",  # Header line for the ad

        # Ad Metadata
        "ident",  # Unique identifier for the ad
        "name",  # Display name for the ad

    ]

    class Timeframe:
        """
        Set of days that an Ad should play, conforming to a List[DaySchedules].
        Starts playing ads on start_day, stops playing ads after end_day.
        """
        __slots__ = ["start_day", "end_day", "schedule"]

        class DaySchedule:
            """
            Amount of times a day (and which day) an ad should play for. The
            WEEKDAYSSTATUS v6 value can be represented by empty List[Runtime].
            """

            __slots__ = ["weekday", "runtimes"]

            class Runtime:
                """
                24-hour timeframe when an ad should start playing and when it
                should stop playing.

                start: Tuple[start_hour: int, start_minute: int]
                end: Tuple[end_hour: int, end_minute: int]
                """

                __slots__ = ["start", "end"]

                def __init__(self, start: Tuple[int, int],
                             end: Tuple[int, int]):
                    self.start = start
                    self.end = end

            class Weekday(Enum):
                SUNDAY = auto()
                MONDAY = auto()
                TUESDAY = auto()
                WEDNESDAY = auto()
                THURSDAY = auto()
                FRIDAY = auto()
                SATURDAY = auto()

            def __init__(self, weekday: Weekday, runtimes: List[Runtime]):
                self.weekday = weekday
                self.runtimes = runtimes

        def __init__(self, start_day: datetime, end_day: datetime,
                     schedule: List[DaySchedule]):
            self.start_day = start_day
            self.end_day = end_day
            self.schedule = schedule

    class Media:
        __slots__ = ["media_resource", "is_sound_enabled"]

        def __init__(self, media_resource: str, is_sound_enabled: bool):
            self.media_resource = media_resource
            self.is_sound_enabled = is_sound_enabled

    def __init__(self,
                 timeframe: Timeframe,
                 playtime: int,
                 background: Media,
                 media: List[Media],
                 lines: List[str],
                 title: str,
                 ident: str,
                 name: str):
        self.timeframe = timeframe
        self.playtime = playtime
        self.background = background
        self.media = media
        self.lines = lines
        self.title = title
        self.ident = ident
        self.name = name


# Good news! I can have a generic AdsConfig based on Config. I can re-use this
# for each specific type of AdsConfig


class AdsBaseConfig(Config):
    """
    This should not be instantiated directly. You should instead create an
    AdsConfig(), an AdsVerticalConfig(), or an AdsHorizontalConfig().
    """
    __slots__ = []

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.ads = config["ads"]

    @staticmethod
    def from_v6_values(data):
        ads = []
        for ad in data["ADS"]:
            start_day = datetime.strptime(ad["STARTDATE"], "%m/%d/%Y")
            end_day = datetime.strptime(ad["ENDDATE"], "%m/%d/%Y")
            schedules = []
            for day_str, runtimes_list in ad["SCHEDULE"].items():
                day = Ad.Timeframe.DaySchedule.Weekday[day_str]
                runtimes = []
                for runtime_dict in runtimes_list:
                    _open, close = runtime_dict["OPEN"], runtime_dict["CLOSE"]
                    runtime = Ad.Timeframe.DaySchedule.Runtime(
                        (int(_open["HOUR"]), int(_open["MIN"])),
                        (int(close["HOUR"]), int(close["MIN"])))
                    runtimes.append(runtime)
                day_schedule = Ad.Timeframe.DaySchedule(day, runtimes)
                schedules.append(day_schedule)
            timeframe = Ad.Timeframe(start_day, end_day, schedules)
            if ad["RUNTIMEAUTO"]:
                playtime = 0
            else:
                playtime = ad["RUNTIMEINTERVAL"]

            background = Ad.Media(ad["BACKGROUND"], ad["BACKGROUNDSOUND"])
            media_list = []
            for i, media in enumerate(ad["MEDIA"]):
                media_list.append(Ad.Media(media, ad["MEDIASOUND"][i]))
            lines = ad["LINES"]
            title = ad["TITLE"]
            ident = ad["IDENT"]
            name = ad["NAME"]

            ads.append(Ad(timeframe, playtime, background, media_list, lines,
                          title, ident, name))

        return {
            "ads": ads
        }

    def to_v6_values(self):
        return {
            "ADS": []
        }


class AdsConfig(AdsBaseConfig):
    """
    Ads configuration for a 16/9 or close aspect ratio display.
    """
    __slots__ = ["ads"]
    # Multiple file_paths incase a user has not saved an advanced config
    file_path = ["home/mediapanel/themes/displayAD/adsConfig_adv.json",
                 "home/mediapanel/themes/displayAD/adsConfig.json"]


class AdsVerticalConfig(AdsBaseConfig):
    """
    Ads configuration for a primarily vertical aspect ratio.  Aspect ratio
    should depend heavily on the LayoutConfig the app will be running on.
    """
    __slots__ = ["ads"]
    # Multiple file_paths incase a user has not saved an advanced config
    file_path = [
            "home/mediapanel/themes/displayAD/adsConfig_adv_vertical.json",
            "home/mediapanel/themes/displayAD/adsConfig_vertical.json"]


class AdsHorizontalConfig(AdsBaseConfig):
    """
    Ads configuration for a primarily horizontal aspect ratio. Aspect ratio
    should depend heavily on the LayoutConfig the app will be running on.
    """
    __slots__ = ["ads"]
    # Multiple file_paths incase a user has not saved an advanced config
    file_path = [
            "home/mediapanel/themes/displayAD/adsConfig_adv_horizontal.json",
            "home/mediapanel/themes/displayAD/adsConfig_horizontal.json"]

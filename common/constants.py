class FieldConstants:
    MAX_VALUE_LENGTH = 24
    MAX_USERNAME_LENGTH = 30
    MAX_NAME_LENGTH = 64
    MAX_LENGTH = 255
    DATE_FORMAT = "%d-%m-%Y"  # 15-12-2012
    TIME_FORMAT = "%H:%M"  # 12:23

    FULL_DATE_FORMAT = "%B %d, %Y"  # November 19, 2021
    FULL_DATE_FORMAT_WITH_DAY = "%d %b %Y, %a"  # Jan. 28 2019, Thu

    DATE_TIME_FORMAT = f"{DATE_FORMAT} %I:%M %p"  # 15-12-2012 01:18 AM
    ALMOST_FULL_DATE_TIME_FORMAT = (
        f"%b %d, %Y, %I:%M %p"  #  Sep 29, 2023, 04:51 PM
    )
    FULL_TIME_FORMAT = "%H:%M:%S %p"  # 12:34:56 AM
    FULL_DATE_TIME_FORMAT = (
        f"{FULL_DATE_FORMAT} %I:%M:%S %p"  # October 23, 2022, 12:49 p.m.
    )


class PostType:
    TEXT = "text"
    IMAGE = "image"
    LINK = "link"
    VIDEO = "video"

    @classmethod
    def values(self) -> list[str]:
        return [self.TEXT, self.IMAGE, self.LINK, self.VIDEO]

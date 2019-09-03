# pylint: disable=missing-docstring
from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP, ForeignKey

import sqlalchemy.sql.functions as func

from .base import Base


# pylint: disable=too-few-public-methods,missing-docstring
class MediaConvertQueue(Base):
    __tablename__ = "mediaConvertQueue"
    id = Column(Integer, primary_key=True)
    upload_timestamp = Column("uploadTimestamp", TIMESTAMP, nullable=False,
                              server_default=func.now(),
                              default=func.now())
    convert_timestamp = Column("convertTimestamp", TIMESTAMP, nullable=True)
    client_id = Column("clientId", Integer, nullable=False)
    device_id = Column("deviceID", String(45), ForeignKey("devices.deviceID"),
                       nullable=True)
    group_id = Column("groupID", Integer, ForeignKey("groups.groupID"),
                      nullable=True)

    filename = Column("fileName", String(1024), nullable=False)
    filepath = Column("filePath", String(1024), nullable=False)
    status = Column(String(128), nullable=False)
    mode = Column(String(128), nullable=False)

    is_digital_frame = Column("app_digitalFrame", Boolean, nullable=False)
    is_display_ad = Column("app_displayAD", Boolean, nullable=False)
    is_alerts = Column("app_alerts", Boolean, nullable=False)
    is_jukebox = Column("app_jukebox", Boolean, nullable=False)

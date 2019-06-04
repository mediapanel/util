# pylint: disable=missing-docstring
from sqlalchemy import (Column, Integer, Boolean, String, Float, TIMESTAMP,
                        ForeignKey)

import sqlalchemy.sql.functions as func

from .base import Base


class Asset(Base):  # pylint: disable=too-few-public-methods,missing-docstring
    __tablename__ = "userAssets"
    id = Column(Integer, primary_key=True)
    client_id = Column("clientId", Integer, nullable=False)
    device_id = Column("deviceID", String(45), ForeignKey("devices.deviceID"),
                       nullable=True)
    group_id = Column("groupID", Integer, ForeignKey("groups.groupID"),
                      nullable=False)
    filename = Column("fileName", String(1024), nullable=False)
    is_digital_frame = Column("app_digitalFrame", Boolean, nullable=False)
    is_display_ad = Column("app_displayAD", Boolean, nullable=False)
    is_alerts = Column("app_alerts", Boolean, nullable=False)
    is_jukebox = Column("app_jukebox", Boolean, nullable=False)
    filetype = Column("fileType", String(11), nullable=False)
    display_name = Column("displayName", String(1024), nullable=True)
    thumbnail_name = Column("thumbName", String(1024), nullable=False)
    timestamp = Column("timeStamp", TIMESTAMP, nullable=False,
                       server_default=func.now(),
                       onupdate=func.now())
    size = Column("MB", Float, nullable=False)

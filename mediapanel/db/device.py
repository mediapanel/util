# pylint: disable=missing-docstring
from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Base


class Device(Base):  # pylint: disable=too-few-public-methods,missing-docstring
    __tablename__ = "devices"
    device_id = Column("deviceID", String(45), primary_key=True)
    client_id = Column("clientID", Integer, nullable=False)

    # last time the device hit responder
    last_ping = Column("lastCheckInTime", TIMESTAMP, nullable=True)
    # nickname given to device
    nickname = Column(String(128), nullable=True)

    # command to run on device ping
    command = Column(String(500), nullable=True)

    system_version = Column("systemVersion", String(30), nullable=True)
    device_ip = Column("deviceIP", String(45), nullable=True)

    # whether or not to update content or settings
    update_content = Column("updateContent", Boolean, nullable=True)
    update_settings = Column("updateSettings", Boolean, nullable=True)

    # whether or not to run a system upgrade
    # 1: upgrade, package install, reboot
    # 2: upgrade, reboot
    # 3: soft upgrade, don't use this, it breaks things, devices need reboot
    update_system = Column("updateSystem", Integer, nullable=True)

    uname = Column("uName", String(256), nullable=False)

    # ::TODO::
    # figure out the purpose of `logo` and `browser`

    assets = relationship("Asset")

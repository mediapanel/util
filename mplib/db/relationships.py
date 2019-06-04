# pylint: disable=missing-docstring,invalid-name
from sqlalchemy import Table, Column, String, Integer, ForeignKey

from .base import Base

device2group = Table(
    "device2groups",
    Base.metadata,
    Column("deviceID", String(45), ForeignKey("devices.deviceID")),
    Column("groupID", Integer, ForeignKey("groups.groupID"))
)

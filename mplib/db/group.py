# pylint: disable=missing-docstring,invalid-name
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .relationships import device2group


class Group(Base):  # pylint: disable=too-few-public-methods,missing-docstring
    __tablename__ = "groups"
    group_id = Column("groupID", Integer, primary_key=True)
    group_name = Column("groupName", String(255), nullable=True)
    client_id = Column("clientID", Integer, nullable=False)
    priority = Column(Integer, nullable=True)  # not used

    devices = relationship("Device", secondary=device2group, backref="groups")
    assets = relationship("Asset")

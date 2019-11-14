# pylint: disable=missing-docstring
import enum
from enum import auto

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


# pylint: disable=too-few-public-methods,missing-docstring
class UserType(enum.Enum):
    client = auto()
    user = auto()


class AlertTypes(enum.IntFlag):
    ads = auto()


class User(Base):  # pylint: disable=too-few-public-methods,missing-docstring
    __tablename__ = "users"
    user_id = Column("userID", Integer, primary_key=True)
    client_id = Column("clientID", Integer, ForeignKey('clients.clientID'))
    client = relationship("Client")
    type = Column(Enum(UserType), nullable=False)  # options: [client, user]

    first_name = Column("firstName", String(45), nullable=False)
    last_name = Column("lastName", String(45), nullable=False)
    email = Column(String(45), nullable=False)
    password = Column(String(128), nullable=False)
    salt = Column(String(15), nullable=False)

    # flags for getting email alerts
    # see: AlertTypes
    get_alert_emails = Column("getAlertEmails", Integer, nullable=False)
